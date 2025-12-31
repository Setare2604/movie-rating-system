from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.handlers import http_exception_handler, validation_exception_handler

from app.controller.movie_controller import router as movie_router
from app.controller.rating_controller import router as rating_router
app = FastAPI(title="Movie Rating System", version="1.0.0")

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(movie_router)
app.include_router(rating_router)

@app.get("/health")
def health():
    return {"status": "ok"}