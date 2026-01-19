import httpx
import json
import os
import asyncio
from typing import Dict, Any, List, Optional

class OllamaService:
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("MODEL_NAME", "medgemma:7b-q4_k_m")
        self.queue = asyncio.Queue()
        self.batch_size = 5
        self.wait_time = 0.1  # seconds
        try:
            asyncio.create_task(self._batch_worker())
        except RuntimeError:
            # No event loop running (common during test collection or script execution)
            pass

    async def _batch_worker(self):
        while True:
            batch = []
            # Wait for at least one item
            item = await self.queue.get()
            batch.append(item)
            
            # Try to get more items until batch_size or wait_time
            start_time = asyncio.get_event_loop().time()
            while len(batch) < self.batch_size:
                try:
                    remaining_time = self.wait_time - (asyncio.get_event_loop().time() - start_time)
                    if remaining_time <= 0:
                        break
                    item = await asyncio.wait_for(self.queue.get(), timeout=remaining_time)
                    batch.append(item)
                except asyncio.TimeoutError:
                    break
            
            # Process batch (Ollama doesn't support list of prompts in one call, 
            # but we can parallelize or if using a different engine, use true batching)
            # For Ollama, we'll run them in parallel to maximize throughput if multiple cores/GPUs available
            tasks = [self._process_single(prompt, system_prompt, future) for prompt, system_prompt, future in batch]
            await asyncio.gather(*tasks)

    async def _process_single(self, prompt, system_prompt, future):
        try:
            res = await self._generate_completion_direct(prompt, system_prompt)
            future.set_result(res)
        except Exception as e:
            future.set_exception(e)

    async def _generate_completion_direct(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")

    async def generate_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        future = asyncio.get_event_loop().create_future()
        await self.queue.put((prompt, system_prompt, future))
        return await future

    async def generate_chat(self, messages: List[Dict[str, str]]) -> str:
        url = f"{self.host}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")
