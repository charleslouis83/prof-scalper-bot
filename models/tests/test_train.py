import io
import csv
from unittest import mock
import joblib
import pandas as pd
import numpy as np
from models import train


def test_fetch_features():
    conn = mock.MagicMock()
    df = pd.DataFrame({"a": [1, 2], "label": [0, 1]})
    with mock.patch("pandas.read_sql", return_value=df) as read_sql:
        X, y = train.fetch_features(conn, days=7)
        read_sql.assert_called_once()
    assert list(X.columns) == ["a"]
    assert y.tolist() == [0, 1]


def test_fetch_pca_params():
    r = mock.MagicMock()
    params = {"mean": 0}
    import pickle
    r.get.return_value = pickle.dumps(params)
    result = train.fetch_pca_params(r)
    assert result == params


def test_log_metrics(tmp_path):
    csv_path = tmp_path / "metrics.csv"
    train.log_metrics("lgb", {"accuracy": 0.9, "auc": 0.8}, csv_path)
    with open(csv_path) as f:
        reader = csv.reader(f)
        rows = list(reader)
    assert rows[0] == ["timestamp", "model", "accuracy", "auc"]
    assert rows[1][1] == "lgb"
