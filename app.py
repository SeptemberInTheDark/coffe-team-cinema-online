from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from src.register.router import router as register_router
from src.Users.router import router as user_router
from src.auth.router import router as auth_router

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


templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")


app.include_router(register_router)
app.include_router(user_router)
app.include_router(auth_router)


#exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()}
    )

