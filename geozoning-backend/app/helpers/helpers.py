# alembic/helpers.py

def read_secret(secret_name: str) -> str:
    secret_path = f"/run/secrets/{secret_name}"
    try:
        with open(secret_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        raise RuntimeError(
            f"Secret '{secret_name}' not found at {secret_path}. "
            f"Make sure it is mounted in docker-compose.yml"
        )