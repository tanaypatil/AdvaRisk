#!/bin/bash

# wait for Postgres to start
function postgres_ready() {
  python <<END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="db")
    conn.close()
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  echo >&2 "Postgres is unavailable - sleeping"
  sleep 1
done

gdown https://drive.google.com/uc?id=1OqKczEjltBkWwjTRU4q6vIbpiGJIMWeU
ls /AdvaRisk
rm -rf main/migrations
python manage.py makemigrations main
python manage.py migrate main
python manage.py migrate
echo "#######"
python manage.py load_data & python manage.py runserver 0.0.0.0:8000