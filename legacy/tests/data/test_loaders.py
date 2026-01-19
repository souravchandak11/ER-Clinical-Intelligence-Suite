import pytest
import os
from data.loaders.mimic_loader import MIMICLoader, CheXpertLoader, ESILoader

def test_mimic_loader_deidentification():
    loader = MIMICLoader(data_dir="data/sample")
    note = loader.load_note("123")
    assert "[DATE]" not in note # Assuming de-id works
    assert "Patient" in note

def test_esi_loader_structure():
    loader = ESILoader(data_dir="data/sample")
    example = loader.get_triage_example("456")
    assert "esi_level" in example
    assert example["esi_level"] in [1, 2, 3, 4, 5]

def test_chexpert_path():
    loader = CheXpertLoader(data_dir="data/sample")
    path = loader.get_image_path("789")
    assert "sample_xray.jpg" in path
