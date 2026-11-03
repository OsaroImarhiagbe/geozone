#!/bin/bash
set -e

MAX_RETRIES=30
RETRY_INTERVAL=2
HOST="${DB_HOST:-postgresql_db}"
PORT="${DB_PORT:-5432}"
count=0

echo "Waiting for PostgreSQL service to start at $HOST:$PORT........"

until (echo > /dev/tcp/"$HOST"/"$PORT") 2>/dev/null; do
    count=$((count + 1))

    if [ "$count" -ge "$MAX_RETRIES" ]; then
        echo "❌ Database did not become ready after $((MAX_RETRIES * RETRY_INTERVAL))s. Exiting."
        exit 1
    fi

    echo "Database is unavailable - retry $count/$MAX_RETRIES..."
    sleep "$RETRY_INTERVAL"
done

echo "PostgreSQL service is ready on  $HOST:$PORT! Continuing...."



echo "🟢 Starting FastAPI server..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload



