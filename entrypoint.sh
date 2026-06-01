#!/bin/bash

set -e

echo "oczekiwanie na uruchomienie bazy danych..."
while ! python manage.py sqlflush > /dev/null 2>&1 ; do
  echo "baza danych jeszcze nie gotowa, czekam 1 sekunde..."
  sleep 1
done
echo "baza danych gotowa"


if [ "$1" = 'python' ]; then
    echo "migracja bazy danych (Tylko kontener WEB)..."
    python manage.py migrate --noinput

    echo "tworzenie konta superusera..."
    python manage.py createsuperuser --noinput || true
else
    echo "kontener pomocniczy wykryty pomijanie migracji"
fi

echo "uruchamianie procesu: $@"
exec "$@"