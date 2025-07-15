import argparse
import cvxpy as cp
import numpy as np
import pandas as pd


def optimize_portfolio(confidence: pd.Series, cov: pd.DataFrame, cvar_limit: float = 0.05, alpha: float = 0.95) -> pd.Series:
    """Optimize portfolio weights with CVaR constraint.

    Parameters
    ----------
    confidence : pd.Series
        Expected returns for each asset.
    cov : pd.DataFrame
        Covariance matrix of asset returns.
    cvar_limit : float, optional
        Maximum allowed CVaR, by default 0.05.
    alpha : float, optional
        Confidence level for CVaR, by default 0.95.

    Returns
    -------
    pd.Series
        Optimized portfolio weights indexed by asset.
    """
    assets = confidence.index
    n = len(assets)
    mu = confidence.values
    sigma = cov.values

    w = cp.Variable(n)

    # simulate scenarios assuming multivariate normal returns
    np.random.seed(42)
    scenarios = np.random.multivariate_normal(mu, sigma, size=500)
    portfolio_returns = scenarios @ w

    t = cp.Variable()
    u = cp.Variable(500)

    cvar = t + cp.sum(u) / (500 * (1 - alpha))

    constraints = [
        cp.sum(w) == 1,
        w >= 0,
        u >= 0,
        u >= -portfolio_returns - t,
        cvar <= cvar_limit,
    ]

    problem = cp.Problem(cp.Maximize(mu @ w), constraints)
    problem.solve()

    return pd.Series(w.value, index=assets)


def main():
    parser = argparse.ArgumentParser(description="Optimize portfolio weights with CVaR constraint")
    parser.add_argument("--conf", required=True, help="CSV file of expected returns")
    parser.add_argument("--cov", required=True, help="CSV file of covariance matrix")
    parser.add_argument("--out", required=True, help="Output CSV for weights")
    args = parser.parse_args()

    conf_df = pd.read_csv(args.conf, index_col=0)
    if conf_df.shape[1] != 1:
        raise ValueError("Expected single column for confidence CSV")
    conf = conf_df.iloc[:, 0]
    cov = pd.read_csv(args.cov, index_col=0)

    weights = optimize_portfolio(conf, cov)
    weights.to_csv(args.out, header=False)


if __name__ == "__main__":
    main()
