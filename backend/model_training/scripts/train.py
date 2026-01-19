import os
import torch
import argparse
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    pipeline,
    logging,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from data.mimic_loader import MIMICDatasetLoader
from data.chexpert_loader import CheXpertLoader
from data.esi_loader import ESIDatasetLoader

def train(args):
    # 1. Load Data
    if args.task == "soap":
        dataset = MIMICDatasetLoader(use_mock=True).data
    elif args.task == "xray":
        dataset = CheXpertLoader(use_mock=True).data
    elif args.task == "triage":
        dataset = ESIDatasetLoader(use_mock=True).data
    else:
        raise ValueError(f"Unknown task: {args.task}")

    # 2. Config Quantization (NF4)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    # 3. Load Model & Tokenizer
    model_id = f"google/medgemma-{args.model_size}"
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    model.config.use_cache = False
    model = prepare_model_for_kbit_training(model)

    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token

    # 4. LoRA Config
    peft_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, peft_config)

    # 5. Training Arguments
    training_args = TrainingArguments(
        output_dir=f"./results_{args.task}",
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=4,
        optim="paged_adamw_32bit",
        save_steps=25,
        logging_steps=10,
        learning_rate=2e-4,
        weight_decay=0.001,
        fp16=True,
        bf16=False,
        max_grad_norm=0.3,
        max_steps=-1,
        warmup_ratio=0.03,
        group_by_length=True,
        lr_scheduler_type="constant",
        report_to="tensorboard"
    )

    # 6. SFT Trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        dataset_text_field="instruction", # Instruction-tuning format
        max_seq_length=512,
        tokenizer=tokenizer,
        args=training_args,
    )

    # 7. Start Training
    print(f"Starting fine-tuning for task: {args.task}...")
    trainer.train()
    
    # 8. Save Model
    model.save_pretrained(f"./medgemma-{args.task}-lora")
    print(f"Training complete. Model saved to ./medgemma-{args.task}-lora")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MedGemma LoRA Fine-tuning Script")
    parser.add_argument("--task", type=str, default="soap", choices=["soap", "xray", "triage"], help="Task to fine-tune on")
    parser.add_argument("--model_size", type=str, default="2b", choices=["2b", "7b"], help="MedGemma model size")
    parser.add_argument("--batch_size", type=int, default=1, help="Training batch size")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--lora_r", type=int, default=16, help="LoRA R parameter")
    parser.add_argument("--lora_alpha", type=int, default=32, help="LoRA Alpha parameter")
    
    args = parser.parse_args()
    train(args)
