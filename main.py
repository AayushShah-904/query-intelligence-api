"""
Query Intelligence API — Development Runner Entry Point

Provides a convenient top-level entry point for launching the local development server.
Executing `python main.py` boots uvicorn with live reloading enabled.
"""

import uvicorn

if __name__ == "__main__":
    # Launch the FastAPI app defined in app.main with hot-reloading
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
