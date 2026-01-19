import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

def load_medgemma_model(model_id: str = "google/medgemma-7b"):
    """
    Loads the MedGemma model with 4-bit quantization for efficient edge deployment.
    """
    print(f"Loading model: {model_id} with 4-bit quantization...")
    
    # Configure 4-bit quantization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    
    return model, tokenizer

if __name__ == "__main__":
    # Example usage (stubs for offline testing)
    print("MedGemma Loader Initialized.")
