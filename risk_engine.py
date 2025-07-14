import json
import threading
import time
from collections import deque
from typing import Optional

import numpy as np
import requests
from flask import Flask, Response
from kafka import KafkaConsumer


class RiskEngine:
    def __init__(self, kafka_servers: Optional[str] = "localhost:9092", pagerduty_url: Optional[str] = None,
                 var_threshold: float = 1.0, es_threshold: float = 1.0, consumer: Optional[KafkaConsumer] = None):
        if consumer is None and kafka_servers is not None:
            self.consumer = KafkaConsumer(
                'trades', 'positions',
                bootstrap_servers=kafka_servers,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest',
                enable_auto_commit=True
            )
        else:
            self.consumer = consumer
        self.pagerduty_url = pagerduty_url
        self.var_threshold = var_threshold
        self.es_threshold = es_threshold
        self.pnl_history = deque(maxlen=1000)
        self.app = Flask(__name__)
        self.app.add_url_rule('/metrics', 'metrics', self.metrics)
        self.app.add_url_rule('/health', 'health', self.health)

    def handle_message(self, data: dict):
        if 'pnl' in data:
            self.pnl_history.append(float(data['pnl']))

    def compute_risk(self):
        if not self.pnl_history:
            return 0.0, 0.0
        losses = -np.array(self.pnl_history)
        var = float(np.quantile(losses, 0.95))
        es = float(losses[losses >= var].mean())
        return var, es

    def check_thresholds(self):
        var, es = self.compute_risk()
        if (var > self.var_threshold or es > self.es_threshold) and self.pagerduty_url:
            try:
                requests.post(self.pagerduty_url, json={'var': var, 'es': es})
            except Exception:
                pass

    def metrics(self):
        var, es = self.compute_risk()
        metrics = f"# HELP portfolio_var Value at Risk\n" \
                  f"# TYPE portfolio_var gauge\nportfolio_var {var}\n" \
                  f"# HELP portfolio_es Expected Shortfall\n" \
                  f"# TYPE portfolio_es gauge\nportfolio_es {es}\n"
        return Response(metrics, mimetype='text/plain')

    def health(self):
        return 'ok'

    def start(self, port: int = 8000):
        if self.consumer is not None:
            def consume_loop():
                for msg in self.consumer:
                    self.handle_message(msg.value)
            threading.Thread(target=consume_loop, daemon=True).start()

        def risk_loop():
            while True:
                time.sleep(60)
                self.check_thresholds()
        threading.Thread(target=risk_loop, daemon=True).start()

        self.app.run(host='0.0.0.0', port=port)


def main():
    engine = RiskEngine()
    engine.start()


if __name__ == '__main__':
    main()
