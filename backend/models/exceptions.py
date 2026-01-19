class MedGemmaError(Exception):
    """Base exception for MedGemma errors."""
    pass

class ModelLoadError(MedGemmaError):
    """Raised when model fails to load."""
    pass

class InferenceError(MedGemmaError):
    """Raised when inference fails."""
    pass

class InsufficientMemoryError(MedGemmaError):
    """Raised when available memory is insufficient."""
    pass

class InvalidInputError(MedGemmaError):
    """Raised when input format is invalid."""
    pass
