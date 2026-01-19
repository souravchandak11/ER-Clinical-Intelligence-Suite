import torch
from datasets import load_dataset
from typing import Dict, List

def format_instruction(task_type: str, input_text: str, target_text: str = None) -> str:
    """
    Formats the clinical input into a prompt structure for MedGemma.
    
    Task Types:
    - 'triage': ESI Level classification (1-5)
    - 'red_flag': Detection of critical conditions
    - 'soap': Generation of SOAP notes
    """
    
    prefix = f"### Task: {task_type.upper()}\n"
    instruction = ""
    
    if task_type == "triage":
        instruction = "Based on the following patient symptoms and vitals, determine the ESI (Emergency Severity Index) level from 1 (highest urgency) to 5 (lowest urgency)."
    elif task_type == "red_flag":
        instruction = "Identify any life-threatening 'red-flag' conditions from the clinical text provided. List them if found, or state 'None'."
    elif task_type == "soap":
        instruction = "Generate a structured SOAP (Subjective, Objective, Assessment, Plan) note from the following clinical notes."
    
    prompt = f"{prefix}### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n"
    
    if target_text:
        prompt += f"{target_text}"
        
    return prompt

def preprocess_function(examples, tokenizer, max_length=1024):
    """
    Tokenizes the formatted prompts for training.
    Assumes examples contain: 'task', 'input', and 'output'
    """
    inputs = []
    for task, clinical_input, clinical_output in zip(examples['task'], examples['input'], examples['output']):
        full_text = format_instruction(task, clinical_input, clinical_output)
        inputs.append(full_text)
    
    model_inputs = tokenizer(
        inputs, 
        max_length=max_length, 
        truncation=True, 
        padding="max_length"
    )
    
    # Labels for casual LLM training should be the same as input_ids
    # but tokens corresponding to the prompt (before Response:) should be ignored (-100)
    # For simplicity in this implementation, we can just copy input_ids 
    # Or implement a more precise label masker if needed for strict instruction tuning.
    model_inputs["labels"] = model_inputs["input_ids"].copy()
    
    return model_inputs

class ClinicalDatasetLoader:
    """
    Handles loading and splitting of clinical datasets.
    """
    def __init__(self, data_path: str = None):
        self.data_path = data_path

    def load_data(self):
        # In a real scenario, this would load from CSV/JSONL
        # For setup, we return dummy/template structure
        if self.data_path:
            return load_dataset("json", data_files=self.data_path)
        else:
            # Placeholder or raise error
            raise ValueError("Data path must be provided for clinical dataset loading.")
