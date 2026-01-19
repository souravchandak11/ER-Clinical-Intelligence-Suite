import pytest
from pydantic import ValidationError
from backend.app.main import Vitals

def test_vitals_valid():
    vitals_data = {
        "hr": 80,
        "bp_sys": 120,
        "bp_dia": 80,
        "spo2": 98,
        "temp": 98.6,
        "rr": 16
    }
    vitals = Vitals(**vitals_data)
    assert vitals.hr == 80

def test_vitals_invalid_hr():
    with pytest.raises(ValidationError):
        Vitals(hr=350, bp_sys=120, bp_dia=80, spo2=98, temp=98.6, rr=16)

def test_vitals_invalid_spo2():
    with pytest.raises(ValidationError):
        Vitals(hr=80, bp_sys=120, bp_dia=80, spo2=105, temp=98.6, rr=16)

def test_vitals_missing_field():
    with pytest.raises(ValidationError):
        Vitals(hr=80, bp_sys=120, bp_dia=80, spo2=98, temp=98.6) # Missing rr
