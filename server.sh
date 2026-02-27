#!/bin/bash

echo "Starting the application..."

CUDA_VISIBLE_DEVICES=1 gunicorn 'app:create_app()' --port 9600 &