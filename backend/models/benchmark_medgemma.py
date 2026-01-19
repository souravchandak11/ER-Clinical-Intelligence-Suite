import time
import torch
import psutil
import argparse
import sys
from medgemma_loader import MedGemmaLoader
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.logger import setup_logger

logger = setup_logger("medgemma_benchmark")

def benchmark_inference(
    model_name="google/medgemma-2b",
    quantization="4bit",
    device="auto",
    num_runs=5
):
    """Run performance benchmarks on MedGemma."""
    
    print(f"Starting benchmark for {model_name} with {quantization} quantization on {device}...")
    
    # Measure Load Time
    try:
        loader = MedGemmaLoader(
            model_name=model_name,
            quantization=quantization,
            device=device
        )
        start_load = time.time()
        loader.load_model()
        load_time = time.time() - start_load
        print(f"Model Load Time: {load_time:.2f}s")
        
        info = loader.get_model_info()
        print(f"Memory Usage: RAM={info['memory_usage']['ram_used_gb']}GB")
        if "gpu_allocated_gb" in info["memory_usage"]:
            print(f"GPU Memory: {info['memory_usage']['gpu_allocated_gb']}GB")

        # Measure Inference
        prompts = [
            "Patient presents with chest pain.",
            "Explain the treatment for hypertension.",
            "What are the symptoms of acute appendicitis?",
        ]
        
        total_tokens = 0
        total_time = 0
        
        print("\nRunning inference benchmarks...")
        for i in range(num_runs):
            prompt = prompts[i % len(prompts)]
            result = loader.generate_text(prompt, max_new_tokens=50)
            
            gen_time = result["generation_time"]
            tokens = result["tokens_used"]
            tps = tokens / gen_time
            
            total_tokens += tokens
            total_time += gen_time
            
            print(f"Run {i+1}: {tokens} tokens in {gen_time:.2f}s ({tps:.2f} tokens/s)")
            
        avg_tps = total_tokens / total_time
        print(f"\nAverage Speed: {avg_tps:.2f} tokens/s")
        print(f"Total Time: {total_time:.2f}s for {total_tokens} tokens")
        
    except Exception as e:
        logger.error(f"Benchmark failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="google/medgemma-2b")
    parser.add_argument("--quantization", default="4bit")
    parser.add_argument("--device", default="auto")
    args = parser.parse_args()
    
    benchmark_inference(args.model, args.quantization, args.device)
