from fastapi import HTTPException, Request, WebSocket, WebSocketDisconnect
from ..devices import sound_sensor
from ..realtime.websocket_manager import active_connections
from ..services.game_service import save_calibration

def register_routes(app):
    @app.post("/api/calibration/manual")
    async def save_manual_calibration(request: Request):
        body = await request.json()
        try:
            threshold = int(body.get("threshold", 50))
        except (TypeError, ValueError):
            raise HTTPException(status_code=422, detail="Threshold must be an integer.")
        if not 30 <= threshold <= 750:
            raise HTTPException(
                status_code=422,
                detail="Threshold must be between 30 and 750.",
            )
        save_calibration(threshold)
        return "Calibration saved."

    @app.websocket("/ws")
    async def calibration_websocket(websocket: WebSocket):
        await websocket.accept()
        active_connections.append(websocket)
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            pass
        finally:
            if websocket in active_connections:
                active_connections.remove(websocket)

    @app.post("/api/calibration/automatic")
    async def run_automatic_calibration():
        duration_seconds = 10
        threshold = await sound_sensor.calibration(duration_seconds)
        threshold = max(30, min(750, threshold))
        save_calibration(int(threshold))
        return "Automatic calibration complete."
