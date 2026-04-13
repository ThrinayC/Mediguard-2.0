import numpy as np
import pandas as pd
import joblib
import os
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

df = pd.read_csv("thyroid_cancer_risk_data (1).csv")

#dropping unrealated columns for quesionare mode - most people wont have this data


df = df.drop(columns=["Patient_ID"])
df = df.drop(columns=["Country"])
df = df.drop(columns=["TSH_Level"])
df = df.drop(columns=["T3_Level"])
df = df.drop(columns=["T4_Level"])
df = df.drop(columns=["Thyroid_Cancer_Risk"])

# mapping binary columns 

df["Gender"] = df["Gender"].map({
    "Male": 1,
    "Female": 0
})

binary_cols = [
    "Family_History",
    "Radiation_Exposure",
    "Iodine_Deficiency",
    "Smoking",
    "Obesity",
    "Diabetes"
]

for col in binary_cols:
    df[col] = df[col].map({"Yes": 1, "No": 0})

df["Diagnosis"] = df["Diagnosis"].map({
    "Benign": 0,
    "Malignant": 1
})
#building ethncity cols

df = pd.get_dummies(
    df,
    columns=["Ethnicity"],
    prefix="Ethnicity",
    drop_first=True
)

eth_cols = df.filter(like="Ethnicity_").columns
df[eth_cols] = df[eth_cols].astype(int)


#building x andd y 

feature_cols = [
    "Age",
    "Gender",
    "Family_History",
    "Radiation_Exposure",
    "Iodine_Deficiency",
    "Smoking",
    "Obesity",
    "Diabetes",
    "Nodule_Size",

    # ethnicity 
    "Ethnicity_Asian",
    "Ethnicity_Caucasian",
    "Ethnicity_Hispanic",
    "Ethnicity_Middle Eastern"
]


y = df["Diagnosis"]
X = df[feature_cols]

#--model training---

#train - test split 

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

#computing class balance weight 

scale_pos_weight = (
    np.sum(y_train == 0) / np.sum(y_train == 1)
)

#training xgboost

model = XGBClassifier(
    n_estimators=150,
    max_depth=4,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42
)

model.fit(X_train, y_train)

#evaluation 


os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/thyroid_questionnaire_xgb.pkl")




