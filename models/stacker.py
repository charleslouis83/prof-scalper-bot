import os
import joblib
import pandas as pd
from xgboost import XGBClassifier


def load_oof_preds():
    lgb = pd.read_csv("models/outputs/lgb/oof_preds.csv")
    cnn = pd.read_csv("models/outputs/cnn/oof_preds.csv")
    lstm = pd.read_csv("models/outputs/lstm/oof_preds.csv")
    X = pd.concat([lgb["pred"], cnn["pred"], lstm["pred"]], axis=1)
    y = lgb["target"]
    return X, y


def train_meta_model():
    X, y = load_oof_preds()
    model = XGBClassifier(eval_metric="logloss")
    model.fit(X, y)
    os.makedirs("models/outputs/stacker", exist_ok=True)
    joblib.dump(model, "models/outputs/stacker/model")
    return model


if __name__ == "__main__":
    train_meta_model()
