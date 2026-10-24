"""Launch SingOnLight in simulation mode for local development."""
import os
import time
import webbrowser
import uvicorn

os.environ["SINGONLIGHT_SIMULATION"] = "1"

if __name__ == "__main__":
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8001")
    uvicorn.run(
        "singonlight.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        reload_dirs=["singonlight"],
    )
