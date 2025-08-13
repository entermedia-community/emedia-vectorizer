#!/bin/bash

echo "Starting the application..."
exec "$@"

gunicorn --workers=1 --timeout=7200 --bind=0.0.0.0:5000 "app:create_app()"
