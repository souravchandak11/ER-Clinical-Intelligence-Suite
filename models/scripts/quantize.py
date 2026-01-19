import os
import subprocess
import argparse

def run_command(command):
    print(f"Executing: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout:
        print(line.decode().strip())
    process.wait()
    if process.returncode != 0:
        print(f"Error: Command failed with return code {process.returncode}")
        return False
    return True

def quantize_model(model_path, output_dir, quant_levels):
    """
    Converts a HuggingFace MedGemma model to GGUF and creates specified quantization levels.
    Requires llama.cpp tools (convert_hf_to_gguf.py and quantize).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Convert HF to F16 GGUF
    f16_output = os.path.join(output_dir, "medgemma-7b-f16.gguf")
    if not os.path.exists(f16_output):
        print("Step 1: Converting HF model to F16 GGUF...")
        convert_cmd = f"python llama.cpp/convert_hf_to_gguf.py {model_path} --outfile {f16_output}"
        if not run_command(convert_cmd):
            return

    # 2. Quantize to requested levels
    for level in quant_levels:
        quant_output = os.path.join(output_dir, f"medgemma-7b-{level}.gguf")
        print(f"\nStep 2: Quantizing to {level}...")
        quant_cmd = f"llama.cpp/quantize {f16_output} {quant_output} {level}"
        run_command(quant_cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quantize MedGemma model to GGUF format.")
    parser.add_argument("--model_path", type=str, required=True, help="Path to the HuggingFace MedGemma model directory.")
    parser.add_argument("--output_dir", type=str, default="models/gguf", help="Directory to save GGUF models.")
    parser.add_argument("--levels", nargs="+", default=["q4_k_m", "q5_k_m", "q8_0"], help="Quantization levels (e.g., q4_k_m, q8_0).")
    
    args = parser.parse_args()
    
    # Check if llama.cpp is present
    if not os.path.exists("llama.cpp"):
        print("Error: llama.cpp directory not found. Please clone it first.")
        print("git clone https://github.com/ggerganov/llama.cpp.git && cd llama.cpp && make")
    else:
        quantize_model(args.model_path, args.output_dir, args.levels)
