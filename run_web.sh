#!/bin/bash

set -e

cmd="$1"

function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="db")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Waiting for Postgres..."
  sleep 1
done

>&2 echo "Postgres ready!"

python manage.py collectstatic --noinput
python manage.py migrate

exec $cmd
