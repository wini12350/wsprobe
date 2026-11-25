"""Intentionally small local WebSocket lab server for WSProbe."""
from __future__ import annotations
import argparse
import asyncio
import json
from http import HTTPStatus
from websockets.asyncio.server import serve

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_TOKEN = "lab-token"
DEFAULT_ORIGIN = "http://localhost:3000"
MAX_FRAME_BYTES = 65_536

async def process_request(connection, request):
    """Reject missing/incorrect bearer tokens during the HTTP handshake."""
    auth = request.headers.get("Authorization", "")
    expected = f"Bearer {DEFAULT_TOKEN}"
    if auth != expected:
        return connection.respond(HTTPStatus.UNAUTHORIZED, "Missing or invalid lab token\\n")
    return None

async def handler(websocket):
    async for message in websocket:
        if isinstance(message, bytes):
            await websocket.send(json.dumps({"status": "error", "message": "Binary messages are not supported"}))
            continue
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            await websocket.send(json.dumps({"status": "error", "message": "Malformed JSON"}))
            continue
        if not isinstance(data, dict):
            await websocket.send(json.dumps({"status": "error", "message": "Expected a JSON object"}))
            continue
        if data.get("type") != "chat":
            await websocket.send(json.dumps({"status": "error", "message": "Unexpected or missing message type"}))
            continue
        await websocket.send(json.dumps({"status": "ok", "message": "Valid message received"}))

async def run_server(host: str, port: int):
    async with serve(
        handler,
        host,
        port,
        origins=[DEFAULT_ORIGIN],
        process_request=process_request,
        max_size=MAX_FRAME_BYTES,
        ping_interval=20,
        ping_timeout=20,
    ):
        print(f"[+] WSProbe lab server listening at ws://{host}:{port}")
        print(f"[+] Allowed Origin: {DEFAULT_ORIGIN}")
        print(f"[+] Lab token: {DEFAULT_TOKEN}")
        print("[+] Press Ctrl+C to stop.")
        await asyncio.Future()

def main():
    parser = argparse.ArgumentParser(description="Start the local WSProbe practice server.")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port (default: 8765)")
    args = parser.parse_args()
    try:
        asyncio.run(run_server(args.host, args.port))
    except KeyboardInterrupt:
        print("\\n[+] Lab server stopped.")

if __name__ == "__main__":
    main()
