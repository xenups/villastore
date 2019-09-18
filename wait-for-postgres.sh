!/bin/sh
set -e
host="$1"
shift
cmd="$@"
until PGPASSWORD=$123456789 psql -h "$host" -U "user001" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - executing command"
exec $cmd
