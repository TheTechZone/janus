#!/bin/sh
# set -x

until pg_isready; do
  >&2 echo "Postgres is unavailabls - sleeping"
  sleep 2
done

>&2 echo "Postgres is up - running migrations"
# /bin/sh -c "/sqlx migrate run --database-url postgres://postgres@localhost/postgres"
/sqlx migrate run --database-url postgres:///postgres