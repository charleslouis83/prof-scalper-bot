import os
import sys
import json
from unittest import mock

import pandas as pd

# Ensure project root is on the import path so the feature_store package can be
# imported when tests are executed from this directory.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

from feature_store import pca


class DummyRedis(dict):
    def set(self, key, value):
        self[key] = value


def test_compute_pca_and_store():
    data = pd.DataFrame({
        'a': [1, 2, 3, 4, 5],
        'b': [2, 3, 4, 5, 6],
        'c': [10, 10, 10, 10, 10],
    })

    with mock.patch('feature_store.pca.client.get_postgres') as get_pg, \
            mock.patch('feature_store.pca.client.get_redis') as get_redis:
        get_pg.return_value.cursor.return_value.__enter__.return_value.fetchall.return_value = [
            ({'a': int(row.a), 'b': int(row.b), 'c': int(row.c)},) for row in data.itertuples()
        ]
        get_redis.return_value = DummyRedis()

        params = pca.run()
        stored = get_redis.return_value['pca:params']
        loaded = json.loads(stored)

        assert 'components' in loaded
        for ratio in loaded['explained_variance_ratio']:
            assert ratio >= 0.01
