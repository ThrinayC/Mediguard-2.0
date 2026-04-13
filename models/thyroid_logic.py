import joblib
import numpy as np
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "thyroid_questionnaire_xgb.pkl"

_model = None

def get_thyroid_model():
    """Load and return the thyroid model."""
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def predict_thyroid_risk(
    age,
    gender,
    family_history,
    radiation_exposure,
    iodine_deficiency,
    smoking,
    obesity,
    diabetes,
    nodule_size,
    ethnicity
):
    """
    Predict thyroid cancer malignancy risk.
    
    Args:
        age: int (18-90)
        gender: int (1=Male, 0=Female)
        family_history: int (1=Yes, 0=No)
        radiation_exposure: int (1=Yes, 0=No)
        iodine_deficiency: int (1=Yes, 0=No)
        smoking: int (1=Yes, 0=No)
        obesity: int (1=Yes, 0=No)
        diabetes: int (1=Yes, 0=No)
        nodule_size: float (0.0-10.0 cm)
        ethnicity: str ("African", "Asian", "Caucasian", "Hispanic", "Middle Eastern")
    
    Returns:
        float: Probability of malignancy (0.0 to 1.0)
    """
    model = get_thyroid_model()
    
    # Ethnicity encoding (African is baseline, all zeros)
    ethnicity_map = {
        "Asian": [1, 0, 0, 0],
        "Caucasian": [0, 1, 0, 0],
        "Hispanic": [0, 0, 1, 0],
        "Middle Eastern": [0, 0, 0, 1],
        "African": [0, 0, 0, 0]
    }
    
    eth_vals = ethnicity_map.get(ethnicity, [0, 0, 0, 0])
    
    # Build feature array
    x = np.array([[
        age,
        gender,
        family_history,
        radiation_exposure,
        iodine_deficiency,
        smoking,
        obesity,
        diabetes,
        nodule_size,
        *eth_vals
    ]])
    
    # Predict probability of malignancy
    prob = model.predict_proba(x)[0][1]
    
    return float(round(prob, 3))