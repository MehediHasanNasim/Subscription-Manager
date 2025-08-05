#!/bin/sh

# wait-for-db.sh

set -e

host="$1"
shift
cmd="$@"

# Use root user and password from environment variables
until mysqladmin ping -h "$host" -u root -p"$MYSQL_ROOT_PASSWORD" --silent; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 2
done

>&2 echo "MySQL is up - executing command"
exec $cmd