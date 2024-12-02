from pathlib import Path

import uvicorn

from app.core.run_app import register_app


app = register_app()


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
