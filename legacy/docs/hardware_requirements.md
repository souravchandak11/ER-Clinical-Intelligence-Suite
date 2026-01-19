# Hardware Requirements for Offline Deployment

To run the ER Clinical Intelligence Suite (including MedGemma-7B quantized models) effectively offline, the following hardware is recommended.

## Minimum Requirements
*Ideal for testing and development on a budget.*

- **CPU**: 4-core Intel Core i5/i7 or AMD Ryzen 5 (Zen 2 or newer)
- **RAM**: 16 GB (preferably 3200MHz+)
- **Storage**: 50 GB SSD (NVMe preferred for fast model loading)
- **GPU**: NVIDIA GTX 1660 Ti or better (6GB VRAM) or Apple M1/M2/M3 with 16GB Unified Memory.
- **Notes**: 4-bit (q4_k_m) models will fit in ~5GB VRAM or ~8GB RAM. Expect 5-10 tokens/sec on CPU transition.

## Recommended Requirements
*Recommended for production-grade clinical performance.*

- **CPU**: 8-core Intel Core i9 or AMD Ryzen 7/9
- **RAM**: 32 GB or 64 GB 
- **Storage**: 100 GB NVMe Gen4 SSD
- **GPU**: NVIDIA RTX 3060/4060 (12GB VRAM) or RTX 3080/4080 (16GB VRAM)
- **Notes**: Allows running 8-bit (q8_0) models entirely in VRAM. Expect 20-40 tokens/sec. 

## Affordable Workstation Guide (~$1500)
A professional-grade offline workstation can be built for approximately $1500:

| Component | Example Model | Approx. Price |
| :--- | :--- | :--- |
| **CPU** | AMD Ryzen 7 7700X | $300 |
| **GPU** | NVIDIA RTX 4060 Ti (16GB) | $450 |
| **Motherboard** | B650 ATX | $180 |
| **RAM** | 64GB DDR5-6000 | $200 |
| **Storage** | 2TB NVMe SSD | $120 |
| **Case/PSU** | Mid Tower + 750W Gold | $250 |
| **Total** | | **~$1500** |

> [!TIP]
> Prioritize GPU VRAM over CPU speed for LLM inference. A 16GB VRAM card (like the 4060 Ti) allows running 8-bit models with large context windows comfortably.
