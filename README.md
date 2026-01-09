# Mini Script Server

Dockerized HTTP server that serves the mini.py script for on-demand execution via curl.

## What is this?

A lightweight container that serves `mini.py` over HTTP, enabling:

- `curl https://yourdomain.com | python3` - Fetch and execute immediately
- SSH tunnel for local port forwarding: `ssh -L 3000:localhost:3000 user@server`

## Quick Start

### Build and Run

```bash
# Build the Docker image
docker build -t mini-script-server .

# Run the container
docker run -d -p 8080:8080 --name script-server mini-script-server
```

### SSH Tunnel + Execute

From your local machine:

```bash
# 1. Establish SSH tunnel (keeps running)
ssh -L 3000:localhost:3000 user@server

# 2. Fetch and run the script
curl https://yourdomain.com | python3
```

The script will execute a reverse proxy on localhost:3000, listening on port 3000.

### Requirements
- `python` on your server

## Files

- `mini.py` - The minified script (reverse proxy for perplexity.ai)
- `server.py` - HTTP server that serves mini.py
- `Dockerfile` - Container configuration

## How It Works

1. Docker container runs a Python HTTP server on port 8080
2. Server responds to GET requests on `/` with the mini.py content
3. curl fetches the script and pipes it to python
4. python executes the script (reverse proxy starts on localhost:3000)

## Use Case

This pattern is useful for:
- Self-hosting scripts
- Portable tool distribution
- Executing code through SSH tunnels
- Quick deployments without file transfer
