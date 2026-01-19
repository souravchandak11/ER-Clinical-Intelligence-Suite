import os
import torch
import yaml
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from data_utils import ClinicalDatasetLoader, preprocess_function
from eval_metrics import compute_metrics
import tensorboard

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def train():
    # 1. Load Configuration
    config = load_config("c:/Users/soura/ER Clinical Intelligence Suite/models/configs/training_config.yaml")
    
    # 2. Setup Quantization (QLoRA)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=config['qlora_config']['quantization_4bit'],
        bnb_4bit_compute_dtype=getattr(torch, config['qlora_config']['bnb_4bit_compute_dtype']),
        bnb_4bit_quant_type=config['qlora_config']['bnb_4bit_quant_type'],
        bnb_4bit_use_double_quant=config['qlora_config']['bnb_4bit_use_double_quant']
    )
    
    # 3. Load Model and Tokenizer
    model_id = config['model_settings']['model_id']
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto", # Automatically assigns to GPU/CPU
        trust_remote_code=True
    )
    model = prepare_model_for_kbit_training(model)
    
    # 4. Setup LoRA
    peft_config = LoraConfig(
        r=config['lora_config']['r'],
        lora_alpha=config['lora_config']['lora_alpha'],
        target_modules=config['lora_config']['target_modules'],
        lora_dropout=config['lora_config']['lora_dropout'],
        bias=config['lora_config']['bias'],
        task_type=config['lora_config']['task_type']
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()
    
    # 5. Load and Preprocess Dataset
    # Placeholder: In production, substitute actual dataset paths
    try:
        loader = ClinicalDatasetLoader(data_path="c:/Users/soura/ER Clinical Intelligence Suite/data/train_data.jsonl")
        dataset = loader.load_data()
        
        tokenized_dataset = dataset.map(
            lambda x: preprocess_function(x, tokenizer),
            batched=True,
            remove_columns=dataset["train"].column_names
        )
    except Exception as e:
        print(f"Warning: Data loading failed ({e}). Proceeding with mock setup for validation...")
        # Mock data for verification purposes if real data isn't present
        from datasets import Dataset, DatasetDict
        mock_data = {
            "task": ["triage", "red_flag", "soap"],
            "input": ["Patient with chest pain.", "Loss of consciousness.", "History of hypertension."],
            "output": ["ESI 2", "Stroke suspected", "SOAP: ..."]
        }
        mock_ds = Dataset.from_dict(mock_data)
        dataset = DatasetDict({"train": mock_ds, "test": mock_ds})
        tokenized_dataset = dataset.map(
            lambda x: preprocess_function(x, tokenizer),
            batched=True,
            remove_columns=dataset["train"].column_names
        )

    # 6. Training Arguments
    training_args = TrainingArguments(
        output_dir=config['model_settings']['output_dir'],
        per_device_train_batch_size=config['training_params']['batch_size'],
        gradient_accumulation_steps=config['training_params']['gradient_accumulation_steps'],
        learning_rate=config['training_params']['learning_rate'],
        num_train_epochs=config['training_params']['num_train_epochs'],
        logging_steps=config['training_params']['logging_steps'],
        eval_strategy=config['training_params']['evaluation_strategy'],
        eval_steps=config['training_params']['eval_steps'],
        save_steps=config['training_params']['save_steps'],
        save_total_limit=config['training_params']['save_total_limit'],
        # TensorBoard logging
        logging_dir=os.path.join(config['model_settings']['output_dir'], "runs"),
        report_to="tensorboard",
        # Accuracy/Optimization
        fp16=True, # T4/V100 support fp16
        push_to_hub=False,
        load_best_model_at_end=True,
        metric_for_best_model="loss"
    )
    
    # 7. Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["test"],
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(
            early_stopping_patience=config['early_stopping_params']['early_stopping_patience']
        )]
    )
    
    # 8. Start Training
    print("Starting MedGemma Fine-tuning...")
    trainer.train()
    
    # 9. Save final model
    trainer.model.save_pretrained(os.path.join(config['model_settings']['output_dir'], "final_model"))
    tokenizer.save_pretrained(os.path.join(config['model_settings']['output_dir'], "final_model"))
    print("Training complete and model saved.")

if __name__ == "__main__":
    train()
