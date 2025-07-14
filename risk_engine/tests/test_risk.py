import os
import sys
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
import risk_engine


def test_risk_metrics():
    engine = risk_engine.RiskEngine(kafka_servers=None, consumer=None, pagerduty_url=None)
    for pnl in [0.1, -0.2, 0.3, -0.1, 0.05]:
        engine.handle_message({'pnl': pnl})
    var, es = engine.compute_risk()
    assert var > 0
    assert es > 0


def test_pagerduty_called(monkeypatch):
    calls = []

    def fake_post(url, json):
        calls.append((url, json))
        class Resp:
            status_code = 200
        return Resp()

    monkeypatch.setattr(risk_engine.requests, 'post', fake_post)
    engine = risk_engine.RiskEngine(kafka_servers=None, consumer=None, pagerduty_url='http://pager', var_threshold=0.0, es_threshold=0.0)
    engine.handle_message({'pnl': -1.0})
    engine.check_thresholds()
    assert calls

