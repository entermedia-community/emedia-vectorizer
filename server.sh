#!/bin/bash

echo "Starting the application..."
exec "$@"

CUDA_VISIBLE_DEVICES=1 uvicorn 'app:create_app()' --port 9600 &