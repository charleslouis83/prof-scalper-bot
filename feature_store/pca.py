import json
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from . import client


def load_features(conn) -> pd.DataFrame:
    """Load all feature rows from the database and return a DataFrame."""
    with conn.cursor() as cur:
        cur.execute("SELECT data FROM features")
        rows = cur.fetchall()
    records = [row[0] for row in rows]
    return pd.DataFrame(records)


def compute_pca(df: pd.DataFrame) -> dict:
    """Compute PCA on dataframe after standardizing."""
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)
    pca = PCA()
    pca.fit(scaled)

    # Determine components with at least 1% variance
    indices = [i for i, var in enumerate(pca.explained_variance_ratio_) if var >= 0.01]
    n_components = max(indices) + 1 if indices else 1

    pca = PCA(n_components=n_components)
    pca.fit(scaled)

    return {
        "components": pca.components_.tolist(),
        "mean": scaler.mean_.tolist(),
        "scale": scaler.scale_.tolist(),
        "explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
    }


def run():
    """Run the daily PCA job and store params in Redis."""
    pg = client.get_postgres()
    df = load_features(pg)
    params = compute_pca(df)

    r = client.get_redis()
    r.set("pca:params", json.dumps(params))

    pg.close()
    return params


if __name__ == "__main__":
    run()
