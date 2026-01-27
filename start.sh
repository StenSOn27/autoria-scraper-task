#!/bin/bash
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "Base is ready. Generating migration..."
python -m alembic revision --autogenerate -m "initial migration"

echo "Applying migration..."
python -m alembic upgrade head
