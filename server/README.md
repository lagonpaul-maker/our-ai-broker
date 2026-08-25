# Server Setup & Execution Guide

## Requirements

- Python 3.x
- opencode CLI installed and configured inside Termux / Debian.

## Test OpenCode Integration

Run:

python3 server/test_bridge.py

## Start Local Server

Run:

chmod +x server/run.sh
./server/run.sh

Or:

python3 server/server.py

The server listens on port 8080.
