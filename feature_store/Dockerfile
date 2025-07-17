FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY feature_store ./feature_store
CMD ["python", "-m", "feature_store.pca"]
