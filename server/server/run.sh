#!/bin/bash

echo "Starting AI Broker Backend..."

if ! command -v python3 &> /dev/null
then
    echo "[Error] Python3 could not be found. Please install Python."
    exit 1
fi

cd "$(dirname "$0")"
python3 server.py
