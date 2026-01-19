import sys
import os
import traceback

# Add current directory to path
sys.path.append(os.getcwd())

print("Current imports check:")
print(f"CWD: {os.getcwd()}")

try:
    print("Attempting: from models.preprocessing import MultimodalPreprocessor")
    from models.preprocessing import MultimodalPreprocessor
    print("✅ MultimodalPreprocessor SUCCESS")
except Exception:
    traceback.print_exc()

try:
    print("Attempting: from models.medgemma_loader import MedGemmaLoader")
    from models.medgemma_loader import MedGemmaLoader
    print("✅ MedGemmaLoader SUCCESS")
except Exception:
    traceback.print_exc()
