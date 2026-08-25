# Our AI Broker

A lightweight bridge connecting an Android app to OpenCode running in Termux/Debian.

## App Details

- Package Name: com.ourai.broker
- Compile SDK: 34
- Minimum SDK: 24
- Backend Port: 8080
- API Endpoint: /api/chat

## Quick Start

### Test OpenCode

python3 server/test_bridge.py

### Start the server

python3 server/server.py

Or:

chmod +x server/run.sh
./server/run.sh

## Architecture

Android App → HTTP Bridge → OpenCode CLI → AI Provider
