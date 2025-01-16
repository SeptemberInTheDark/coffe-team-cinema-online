import uvicorn
from starlette.responses import RedirectResponse

from app.core.run_app import register_app


app = register_app()

@app.get("/")
def read_root():
    return RedirectResponse(url="/api/v1/docs")

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
