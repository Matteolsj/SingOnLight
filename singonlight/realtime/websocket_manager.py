from fastapi import WebSocket, WebSocketDisconnect

active_connections: list[WebSocket] = []

async def broadcast(message: str):
    """Send a message to every client connected to the calibration page."""
    for websocket in active_connections.copy():
        try:
            await websocket.send_text(message)
        except (OSError, RuntimeError, WebSocketDisconnect):
            if websocket in active_connections:
                active_connections.remove(websocket)
