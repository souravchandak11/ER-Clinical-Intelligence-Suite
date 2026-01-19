import os
import time
import torch
import psutil
import logging
from typing import Optional, Dict, Union, Any, List
from PIL import Image

try:
    import GPUtil
except ImportError:
    GPUtil = None

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    AutoProcessor
)
from transformers.utils import is_flash_attn_2_available

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.logger import setup_logger
from .config import MedGemmaConfig
from .exceptions import ModelLoadError, InferenceError, InsufficientMemoryError

logger = setup_logger("medgemma_loader")

class MedGemmaLoader:
    """
    Production-ready loader for MedGemma models with quantization support.
    
    Features:
    - Automatic model downloading from Hugging Face
    - 4-bit/8-bit quantization for memory efficiency
    - Model caching to speed up subsequent loads
    - CPU/GPU device management
    - Multimodal support (text + images)
    - Memory profiling
    - Error handling and retries

    Example:
        >>> loader = MedGemmaLoader(quantization="4bit")
        >>> loader.load_model()
        >>> result = loader.generate_text("Patient reports chest pain.")
        >>> print(result["generated_text"])
    """
    
    def __init__(
        self,
        model_name: str = "google/medgemma-2b",
        quantization: str = "4bit",  # "4bit", "8bit", or "none"
        device: str = "auto",  # "cuda", "cpu", or "auto"
        cache_dir: str = "./cache/models",
        max_length: int = 2048,
        load_in_8bit: bool = False,
        load_in_4bit: bool = True,
    ):
        """Initialize the model loader with configuration."""
        self.config = MedGemmaConfig(
            model_name=model_name,
            quantization=quantization,
            device=device,
            cache_dir=cache_dir,
            max_length=max_length,
            load_in_8bit=load_in_8bit,
            load_in_4bit=load_in_4bit
        )
        self.model = None
        self.tokenizer = None
        self.processor = None  # For multimodal
        self.device_map = None
        
        # Override booleans if string quantization is explicit
        if quantization == "4bit":
            self.config.load_in_4bit = True
            self.config.load_in_8bit = False
        elif quantization == "8bit":
            self.config.load_in_4bit = False
            self.config.load_in_8bit = True
        elif quantization == "none":
            self.config.load_in_4bit = False
            self.config.load_in_8bit = False
            
    def _get_quantization_config(self) -> Optional[BitsAndBytesConfig]:
        """Generate the quantization configuration."""
        if self.config.load_in_4bit:
            return BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float16,
                bnb_4bit_use_double_quant=True,
            )
        elif self.config.load_in_8bit:
            return BitsAndBytesConfig(
                load_in_8bit=True,
                llm_int8_threshold=6.0
            )
        return None

    def _log_memory_usage(self):
        """Log current memory usage."""
        # RAM usage
        ram = psutil.virtual_memory()
        logger.info(f"RAM: {ram.percent}% used ({ram.used / 1e9:.2f}GB / {ram.total / 1e9:.2f}GB)")
        
        # GPU usage (if available)
        if torch.cuda.is_available():
            try:
                if GPUtil:
                    gpus = GPUtil.getGPUs()
                    for gpu in gpus:
                        logger.info(f"GPU {gpu.id}: {gpu.memoryUtil*100:.1f}% used ({gpu.memoryUsed}MB / {gpu.memoryTotal}MB)")
                else:
                    # Fallback if GPUtil is not installed
                    logger.info(f"GPU Allocated: {torch.cuda.memory_allocated() / 1e9:.2f}GB")
                    logger.info(f"GPU Reserved: {torch.cuda.memory_reserved() / 1e9:.2f}GB")
            except Exception as e:
                logger.warning(f"Could not log GPU memory: {e}")

    def load_model(self) -> None:
        """
        Load the MedGemma model with specified quantization.
        
        Steps:
        1. Check if model exists in cache
        2. Download from HuggingFace if needed
        3. Apply quantization configuration
        4. Load tokenizer
        5. Warm up model with dummy input
        6. Log memory usage
        
        Raises:
            ModelLoadError: If model fails to load
            InsufficientMemoryError: If not enough RAM/VRAM
        """
        if self.model is not None:
            logger.info("Model already loaded.")
            return

        logger.info(f"Loading model {self.config.model_name} with {self.config.quantization} quantization...")
        self._log_memory_usage()
        
        start_time = time.time()
        
        try:
            quantization_config = self._get_quantization_config()
            
            # Determine device map
            if self.config.device == "auto":
                self.device_map = "auto"
            elif self.config.device == "cuda" and torch.cuda.is_available():
                self.device_map = "cuda"
            else:
                self.device_map = "cpu"
                if self.config.load_in_4bit or self.config.load_in_8bit:
                    logger.warning("Quantization requires GPU. Falling back to non-quantized CPU load.")
                    quantization_config = None
            
            # Load Tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_name,
                cache_dir=self.config.cache_dir,
                token=os.getenv("HF_TOKEN"),
                trust_remote_code=self.config.trust_remote_code
            )
            
            # Load Model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                quantization_config=quantization_config,
                device_map=self.device_map,
                trust_remote_code=self.config.trust_remote_code,
                cache_dir=self.config.cache_dir,
                token=os.getenv("HF_TOKEN"),
                # Use flash attention if available and using CUDA
                attn_implementation="flash_attention_2" if is_flash_attn_2_available() and self.device_map != "cpu" else None
            )
            
            # Try loading processor for multimodal if it exists
            try:
                self.processor = AutoProcessor.from_pretrained(
                    self.config.model_name,
                    cache_dir=self.config.cache_dir,
                    token=os.getenv("HF_TOKEN"),
                    trust_remote_code=self.config.trust_remote_code
                )
            except Exception:
                logger.debug("No processor found (likely text-only model or processor not needed).")
            
            logger.info(f"Model loaded in {time.time() - start_time:.2f}s")
            self._log_memory_usage()
            
            # Warmup
            logger.info("Warming up model...")
            dummy_input = "Hello, doctor."
            inputs = self.tokenizer(dummy_input, return_tensors="pt").to(self.model.device)
            with torch.no_grad():
                self.model.generate(**inputs, max_new_tokens=10)
            logger.info("Warmup complete.")
            
        except torch.cuda.OutOfMemoryError:
            logger.error("Insufficient GPU memory.")
            self.unload_model()
            raise InsufficientMemoryError("Not enough GPU memory to load model.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise ModelLoadError(f"Failed to load model: {e}")

    def generate_text(
        self,
        prompt: str,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        do_sample: bool = True,
    ) -> dict:
        """
        Generate text completion from prompt.
        
        Args:
            prompt: Input text prompt
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            do_sample: Whether to use sampling
            
        Returns:
            dict with:
                - generated_text: The completion
                - tokens_used: Number of tokens
                - generation_time: Time taken in seconds
                - model_info: Model metadata
        """
        if self.model is None:
            raise ModelLoadError("Model is not loaded. Call load_model() first.")
            
        start_time = time.time()
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            input_length = inputs.input_ids.shape[1]
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=do_sample,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            generated_text = self.tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
            total_time = time.time() - start_time
            tokens_generated = outputs.shape[1] - input_length
            
            return {
                "generated_text": generated_text,
                "tokens_used": tokens_generated,
                "generation_time": total_time,
                "model_info": self.get_model_info()
            }
            
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            raise InferenceError(f"Inference failed: {e}")

    def generate_multimodal(
        self,
        text: str,
        image: Image.Image,
        max_new_tokens: int = 512,
    ) -> dict:
        """
        Generate response from text + image input.
        
        Args:
            text: Text query/context
            image: PIL Image object
            max_new_tokens: Max tokens to generate
            
        Returns:
            dict with generated response and metadata
        """
        if self.model is None:
            raise ModelLoadError("Model is not loaded.")
        if self.processor is None:
            # Fallback to text-only if processor not available, or raise error. 
            # Ideally multimodal models have a processor.
            # Assuming if image is passed we MUST use processor or it's a mistargeted call.
            # However, user might pass Paligemma or similar which uses processor.
            raise InferenceError("This model definition does not support multimodal inputs (no processor found).")

        start_time = time.time()
        
        try:
            # Prepare inputs - dependent on specific model (e.g., Paligemma, MedGemmamultimodal)
            # Standard transformers usage for multimodal:
            inputs = self.processor(text=text, images=image, return_tensors="pt").to(self.model.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens
                )
            
            # Decode - usually processor.batch_decode or tokenizer.decode
            generated_text = self.processor.batch_decode(outputs, skip_special_tokens=True)[0]
            # Clean up prompt from output if needed
            # For some models, generated_text includes the prompt
            
            return {
                "generated_text": generated_text,
                "generation_time": time.time() - start_time,
                "model_info": self.get_model_info()
            }
            
        except Exception as e:
            logger.error(f"Multimodal inference failed: {e}")
            raise InferenceError(f"Multimodal inference failed: {e}")

    def get_model_info(self) -> dict:
        """
        Get detailed model information.
        
        Returns:
            dict with parameters, quantization, device, etc.
        """
        if self.model is None:
            return {"loaded": False}
        
        ram = psutil.virtual_memory()  
        
        mem_info = {
            "ram_used_gb": round(ram.used / 1e9, 2),
            "ram_total_gb": round(ram.total / 1e9, 2),
        }
        
        if torch.cuda.is_available():
            mem_info["gpu_allocated_gb"] = round(torch.cuda.memory_allocated() / 1e9, 2)
            mem_info["gpu_reserved_gb"] = round(torch.cuda.memory_reserved() / 1e9, 2)

        return {
            "model_name": self.config.model_name,
            "parameters": f"{sum(p.numel() for p in self.model.parameters())/1e9:.1f}B",
            "quantization": self.config.quantization,
            "device": str(self.model.device),
            "memory_usage": mem_info,
            "max_length": self.config.max_length,
            "loaded": True
        }
    
    def unload_model(self) -> None:
        """Unload model from memory and clear cache."""
        logger.info("Unloading model...")
        if self.model:
            del self.model
            self.model = None
        if self.tokenizer:
            del self.tokenizer
            self.tokenizer = None
        if self.processor:
            del self.processor
            self.processor = None
            
        torch.cuda.empty_cache()
        logger.info("Model unloaded.")

    @staticmethod
    def format_medical_prompt(
        task: str,  # "triage", "documentation", "diagnosis"
        context: Dict[str, Any],
    ) -> str:
        """
        Format prompts for medical tasks following MedGemma best practices.
        
        Templates:
        - Triage: "As an ER triage nurse, analyze..."
        - Documentation: "Generate a SOAP note for..."
        - Diagnosis: "Based on the following clinical presentation..."
        """
        
        templates = {
            "triage": """You are an experienced ER triage nurse. Analyze the following patient presentation and provide:
1. ESI urgency level (1-5)
2. Red-flag conditions to consider
3. Recommended next steps

Patient Information:
{context}

Respond in JSON format.""",
            
            "documentation": """Generate a structured SOAP note from the following clinical encounter:

{context}

Format as:
Subjective: 
Objective:
Assessment:
Plan:""",
        }
        
        # Simple context formatting: if context is dict, convert to pretty string, else use as is
        ctx_str = ""
        if isinstance(context, dict):
             ctx_str = "\\n".join([f"{k}: {v}" for k, v in context.items()])
        else:
             ctx_str = str(context)
             
        return template.format(context=ctx_str)

def load_medgemma_model(
    model_name: str = "google/medgemma-2b",
    quantization: str = "4bit",
    device: str = "auto"
):
    """
    Helper function to load model and tokenizer in one go,
    matching the signature expected by TriageService.
    """
    loader = MedGemmaLoader(model_name=model_name, quantization=quantization, device=device)
    loader.load_model()
    return loader.model, loader.tokenizer
