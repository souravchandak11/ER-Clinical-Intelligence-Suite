import pytest
import time
import torch
from unittest.mock import MagicMock, patch
from .medgemma_loader import MedGemmaLoader
from .exceptions import ModelLoadError, InsufficientMemoryError

# Mock torch.cuda for environments without GPU
if not torch.cuda.is_available():
    torch.cuda.is_available = MagicMock(return_value=False)

class TestMedGemmaLoader:
    
    @pytest.fixture
    def mock_loader(self):
        with patch("transformers.AutoTokenizer.from_pretrained"), \
             patch("transformers.AutoModelForCausalLM.from_pretrained") as mock_model:
            
            # Setup mock model
            mock_model.return_value.device = torch.device("cpu")
            mock_model.return_value.generate.return_value = torch.tensor([[1, 2, 3]])
            mock_model.return_value.parameters.return_value = [torch.tensor([1.0])]
            
            loader = MedGemmaLoader(quantization="none", device="cpu")
            # We don't call load_model here to allow testing it separately
            return loader

    def test_init(self):
        """Test initialization configuration."""
        loader = MedGemmaLoader(model_name="test-model", quantization="4bit")
        assert loader.config.model_name == "test-model"
        assert loader.config.load_in_4bit is True
        assert loader.config.load_in_8bit is False

    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoModelForCausalLM.from_pretrained")
    def test_load_model_success(self, mock_model, mock_tokenizer):
        """Test successful model loading."""
        loader = MedGemmaLoader(device="cpu", quantization="none")
        loader.load_model()
        
        assert loader.model is not None
        assert loader.tokenizer is not None
        assert loader.get_model_info()["loaded"] is True

    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoModelForCausalLM.from_pretrained")
    def test_load_model_failure(self, mock_model, mock_tokenizer):
        """Test model loading failure handling."""
        mock_model.side_effect = Exception("Download failed")
        loader = MedGemmaLoader()
        
        with pytest.raises(ModelLoadError):
            loader.load_model()

    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoModelForCausalLM.from_pretrained")
    def test_generate_text(self, mock_model_cls, mock_tokenizer_cls):
        """Test text generation."""
        # Setup mocks
        mock_model = MagicMock()
        mock_model.device = "cpu"
        # Return a tensor of shape (1, 5) - context + new tokens
        mock_model.generate.return_value = torch.tensor([[101, 200, 201, 202, 102]])
        mock_model_cls.return_value = mock_model
        
        mock_tokenizer = MagicMock()
        mock_tokenizer.return_value = {"input_ids": torch.tensor([[101]])}
        mock_tokenizer.eos_token_id = 102
        mock_tokenizer.decode.return_value = "generated text"
        mock_tokenizer_cls.return_value = mock_tokenizer
        
        loader = MedGemmaLoader(quantization="none")
        loader.load_model()
        
        result = loader.generate_text("Test prompt")
        
        assert result["generated_text"] == "generated text"
        assert "tokens_used" in result
        assert "generation_time" in result

    @patch("transformers.AutoTokenizer.from_pretrained")
    @patch("transformers.AutoModelForCausalLM.from_pretrained")
    def test_memory_info(self, mock_model, mock_tokenizer):
        """Test memory info retrieval."""
        loader = MedGemmaLoader(quantization="none")
        loader.load_model()
        
        info = loader.get_model_info()
        assert "memory_usage" in info
        assert "ram_used_gb" in info["memory_usage"]

    def test_unload_model(self, mock_loader):
        """Test model unloading."""
        # Manually set mocked objects
        mock_loader.model = MagicMock()
        mock_loader.tokenizer = MagicMock()
        
        mock_loader.unload_model()
        
        assert mock_loader.model is None
        assert mock_loader.tokenizer is None

    def test_format_medical_prompt(self):
        """Test prompt formatting."""
        context = {"vitals": "stable", "complaint": "pain"}
        prompt = MedGemmaLoader.format_medical_prompt("triage", context)
        
        assert "experienced ER triage nurse" in prompt
        assert "vitals: stable" in prompt
