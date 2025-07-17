import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import tensorflow as tf

# Make sure the project root is available on the Python path so the model_server
# package can be imported correctly when tests run from this directory.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

from model_server.api import app

client = TestClient(app)


def mock_predict_response(value: float):
    resp = MagicMock()
    resp.outputs = {"probabilities": tf.make_tensor_proto([[value]])}
    return resp


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_endpoint():
    with patch("model_server.api.prediction_service_pb2_grpc.PredictionServiceStub") as stub_cls:
        stub_instance = MagicMock()
        stub_instance.Predict.side_effect = [
            mock_predict_response(0.6),
            mock_predict_response(0.8),
        ]
        stub_cls.return_value = stub_instance

        response = client.post("/predict", json={"features": [1.0, 2.0]})
        assert response.status_code == 200
        data = response.json()
        assert data["confidence"] == pytest.approx(0.7)
        assert data["leverage_band"] == [30, 50, 80, 100]
