import os
from datetime import datetime, timedelta
import csv
import joblib
import pickle
import pandas as pd
import numpy as np
import psycopg2
import redis
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score


def fetch_features(conn, days: int = 7):
    """Fetch feature data from TimescaleDB for the last `days` days."""
    since = datetime.utcnow() - timedelta(days=days)
    query = "SELECT * FROM features WHERE ts >= %s"
    df = pd.read_sql(query, conn, params=(since,))
    X = df.drop(columns=["label"])
    y = df["label"]
    return X, y


def fetch_pca_params(r: redis.Redis):
    """Load PCA parameters stored in Redis using pickle."""
    data = r.get("pca_params")
    if data is None:
        return None
    return pickle.loads(data)


def train_lightgbm(X: pd.DataFrame, y: pd.Series):
    import optuna.integration.lightgbm as lgb

    dtrain = lgb.Dataset(X, label=y)
    params = {"objective": "binary", "metric": "auc"}
    tuner = lgb.LightGBMTuner(params, dtrain, verbose_eval=False)
    tuner.run()
    model = tuner.get_best_booster()
    preds = model.predict(X)
    accuracy = accuracy_score(y, (preds > 0.5).astype(int))
    auc = roc_auc_score(y, preds)
    return model, {"accuracy": accuracy, "auc": auc}


def load_images(image_dir: str):
    import tensorflow as tf

    # `tf.keras.preprocessing.image_dataset_from_directory` is deprecated in
    # recent TensorFlow versions. Use the utils variant to avoid warnings.
    train_ds = tf.keras.utils.image_dataset_from_directory(
        image_dir,
        labels="inferred",
        image_size=(64, 64),
        batch_size=32,
        validation_split=0.2,
        subset="training",
        seed=42,
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        image_dir,
        labels="inferred",
        image_size=(64, 64),
        batch_size=32,
        validation_split=0.2,
        subset="validation",
        seed=42,
    )
    return train_ds, val_ds


def build_cnn():
    import tensorflow as tf

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Conv2D(16, 3, activation="relu", input_shape=(64, 64, 3)),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model


def train_cnn(image_dir: str):
    import tensorflow as tf

    train_ds, val_ds = load_images(image_dir)
    model = build_cnn()
    model.fit(train_ds, validation_data=val_ds, epochs=1)
    preds = model.predict(val_ds)
    y_true = np.concatenate([y.numpy() for _, y in val_ds], axis=0)
    accuracy = accuracy_score(y_true, (preds.ravel() > 0.5).astype(int))
    auc = roc_auc_score(y_true, preds.ravel())
    return model, {"accuracy": accuracy, "auc": auc}


def prepare_sequence_data(df: pd.DataFrame, seq_len: int = 60):
    features = []
    labels = []
    for i in range(len(df) - seq_len):
        features.append(df["return"].iloc[i : i + seq_len].values)
        labels.append(int(df["target"].iloc[i + seq_len]))
    X = np.stack(features)
    y = np.array(labels)
    return X[:, :, None], y


def build_lstm(input_shape):
    import tensorflow as tf

    model = tf.keras.Sequential(
        [
            tf.keras.layers.LSTM(32, input_shape=input_shape),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model


def train_lstm(df: pd.DataFrame):
    X, y = prepare_sequence_data(df)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    model = build_lstm(X_tr.shape[1:])
    model.fit(X_tr, y_tr, epochs=1, validation_data=(X_te, y_te))
    preds = model.predict(X_te)
    accuracy = accuracy_score(y_te, (preds.ravel() > 0.5).astype(int))
    auc = roc_auc_score(y_te, preds.ravel())
    return model, {"accuracy": accuracy, "auc": auc}


def log_metrics(model_name: str, metrics: dict, csv_path: str):
    print(f"{model_name} accuracy: {metrics['accuracy']:.4f}, auc: {metrics['auc']:.4f}")
    exists = os.path.exists(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["timestamp", "model", "accuracy", "auc"])
        writer.writerow([
            datetime.utcnow().isoformat(),
            model_name,
            metrics["accuracy"],
            metrics["auc"],
        ])


def main():
    os.makedirs("models/outputs/lgb", exist_ok=True)
    os.makedirs("models/outputs/cnn", exist_ok=True)
    os.makedirs("models/outputs/lstm", exist_ok=True)

    conn = psycopg2.connect(os.getenv("TS_DB_DSN", ""))
    X, y = fetch_features(conn)
    r = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", 6379))
    )
    fetch_pca_params(r)

    lgb_model, lgb_metrics = train_lightgbm(X, y)
    joblib.dump(lgb_model, "models/outputs/lgb/model")
    log_metrics("lgb", lgb_metrics, "models/outputs/metrics.csv")

    cnn_model, cnn_metrics = train_cnn("data/depth_snapshots")
    cnn_model.save("models/outputs/cnn/model")
    log_metrics("cnn", cnn_metrics, "models/outputs/metrics.csv")

    returns = pd.read_csv("data/returns.csv")
    lstm_model, lstm_metrics = train_lstm(returns)
    lstm_model.save("models/outputs/lstm/model")
    log_metrics("lstm", lstm_metrics, "models/outputs/metrics.csv")


if __name__ == "__main__":
    main()
