import os
import redis
import psycopg2


def get_redis() -> redis.Redis:
    """Return a Redis connection using REDIS_URL env var."""
    url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return redis.Redis.from_url(url)


def get_postgres() -> psycopg2.extensions.connection:
    """Return a PostgreSQL connection using TIMESCALE_URL env var."""
    dsn = os.getenv("TIMESCALE_URL", "dbname=postgres user=postgres host=localhost")
    return psycopg2.connect(dsn)
