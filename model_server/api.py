from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import grpc
import os
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

MODEL_SERVER_ADDRESS = os.getenv("MODEL_SERVER_ADDRESS", "localhost:8500")
MODEL_NAMES = ["model1", "model2"]

app = FastAPI()

class PredictRequest(BaseModel):
    features: List[float]


def _predict_single(model_name: str, features: List[float]) -> float:
    channel = grpc.insecure_channel(MODEL_SERVER_ADDRESS)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    request = predict_pb2.PredictRequest()
    request.model_spec.name = model_name
    request.inputs["features"].CopyFrom(
        tf.make_tensor_proto([features])
    )
    response = stub.Predict(request, timeout=5.0)
    probabilities = tf.make_ndarray(response.outputs["probabilities"])
    return float(probabilities[0][0])


@app.post("/predict")
async def predict(data: PredictRequest):
    probs = []
    for name in MODEL_NAMES:
        prob = _predict_single(name, data.features)
        probs.append(prob)
    confidence = sum(probs) / len(probs) if probs else 0.0
    return {"confidence": confidence, "leverage_band": [30, 50, 80, 100]}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
