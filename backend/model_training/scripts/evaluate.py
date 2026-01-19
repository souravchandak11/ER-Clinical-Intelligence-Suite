import argparse
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from peft import PeftModel
from data.mimic_loader import MIMICDatasetLoader
from data.esi_loader import ESIDatasetLoader
try:
    from rouge_score import rouge_scorer
    HAS_ROUGE = True
except ImportError:
    HAS_ROUGE = False

def evaluate(args):
    # 1. Load Base Model and Adapter
    model_id = f"google/medgemma-{args.model_size}"
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    
    base_model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True
    )
    
    if args.adapter_path:
        print(f"Loading adapter from {args.adapter_path}...")
        model = PeftModel.from_pretrained(base_model, args.adapter_path)
    else:
        print("No adapter provided. Evaluating base model performance...")
        model = base_model

    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

    # 2. Select Test Dataset
    if args.task == "soap":
        test_data = MIMICDatasetLoader(use_mock=True).data[:10] # Small test set
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True) if HAS_ROUGE else None
    elif args.task == "triage":
        test_data = ESIDatasetLoader(use_mock=True).data[:20]
    else:
        print(f"Evaluation for {args.task} not yet implemented.")
        return

    # 3. Inference Loop
    correct = 0
    rouge_scores = {"rouge1": [], "rougeL": []}

    print(f"Running evaluation on {len(test_data)} samples...")
    for item in test_data:
        prompt = item["instruction"]
        expected = item["output"]
        
        result = generator(prompt, max_new_tokens=100, do_sample=False)[0]['generated_text']
        prediction = result.replace(prompt, "").strip()

        if args.task == "triage":
            if expected.lower() in prediction.lower():
                correct += 1
        elif args.task == "soap" and HAS_ROUGE:
            scores = scorer.score(expected, prediction)
            rouge_scores["rouge1"].append(scores['rouge1'].fmeasure)
            rouge_scores["rougeL"].append(scores['rougeL'].fmeasure)

    # 4. Report Metrics
    if args.task == "triage":
        accuracy = correct / len(test_data)
        print(f"Triage Accuracy: {accuracy:.2%}")
    elif args.task == "soap":
        if HAS_ROUGE:
            avg_r1 = sum(rouge_scores["rouge1"]) / len(rouge_scores["rouge1"])
            avg_rl = sum(rouge_scores["rougeL"]) / len(rouge_scores["rougeL"])
            print(f"ROUGE-1: {avg_r1:.4f}")
            print(f"ROUGE-L: {avg_rl:.4f}")
        else:
            print("rouge-score package not installed. Skipping ROUGE calculation.")
            print(f"Sample Prediction: {prediction[:100]}...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MedGemma Evaluation Script")
    parser.add_argument("--task", type=str, default="soap", choices=["soap", "triage"])
    parser.add_argument("--model_size", type=str, default="2b")
    parser.add_argument("--adapter_path", type=str, help="Path to trained LoRA adapter")
    
    args = parser.parse_args()
    evaluate(args)
