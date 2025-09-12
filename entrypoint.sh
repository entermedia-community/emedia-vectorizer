#!/bin/bash

echo "Starting the application..."
exec "$@"

gunicorn -w 2 -t 120 -b 0.0.0.0:5000 'app:create_app()' --error-logfile error.log
