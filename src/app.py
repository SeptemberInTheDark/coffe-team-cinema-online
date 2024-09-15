
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from .Users.models import get_users
from sqlalchemy.orm import Session

try:
    from db import get_db
except ImportError:
    from .db import get_db

import uvicorn

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173" #react
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/test')
async def api_route():
    products = [
        {
            "id": 1,
            "price": 100,
        },
        {
            "id": 2,
            "price": 200,
        },
        {
            "id": 3,
            "price": 300,
        },
    ]
    return {"products": products}


templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/api/users')
def api_users(db: Session = Depends(get_db)):
    users = get_users(db)
    print(users)
    return {"users": users}


#exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status.code,
        content={"detail": exc.detail}
    )


# if __name__ == '__main__':
#     uvicorn.run(
#         "app:app",
#         host='0.0.0.0',
#         # host='localhost',
#         port=8080,
#         log_level="info",
#         reload=False
#     )
