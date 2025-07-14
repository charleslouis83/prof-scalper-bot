FROM tensorflow/serving:latest

# Install python and pip for FastAPI
RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY api.py /app/api.py
COPY models.config /models/models.config

ENV MODEL_CONFIG_FILE=/models/models.config

EXPOSE 8500 8501 8000

CMD tensorflow_model_server --port=8500 --rest_api_port=8501 \
    --model_config_file=${MODEL_CONFIG_FILE} & \
    uvicorn api:app --host 0.0.0.0 --port 8000 --reload
