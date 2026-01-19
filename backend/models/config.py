from dataclasses import dataclass, field
from typing import Optional, List, Union

@dataclass
class MedGemmaConfig:
    """Configuration for MedGemma model loader."""
    model_name: str = "google/medgemma-2b"
    quantization: str = "4bit"  # "4bit", "8bit", "none"
    device: str = "auto"  # "cuda", "cpu", "auto"
    cache_dir: str = "./cache/models"
    max_length: int = 2048
    load_in_8bit: bool = False
    load_in_4bit: bool = True
    trust_remote_code: bool = True
    
@dataclass
class GenerationConfig:
    """Configuration for text generation."""
    max_new_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    do_sample: bool = True
    repetition_penalty: float = 1.1
    
@dataclass
class ModelInfo:
    """Model status and metadata."""
    model_name: str
    parameters: str
    quantization: str
    device: str
    memory_usage: dict
    max_length: int
    loaded: bool = False
