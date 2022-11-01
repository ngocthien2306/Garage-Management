from typing import List
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from fastapi.responses import JSONResponse
from api.face_recognition.face_recognition import face_router
from core.exceptions import CustomException
from core.extension.dependencies.logging import Logging
from api import router
from api.home.home import home_router

def init_routers(app: FastAPI) -> None:
    app.include_router(router)
    app.include_router(home_router)
    
def init_listeners(app: FastAPI) -> None:
    @app.exception_handler(CustomException)
    async def custome_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message}
        )
def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )

def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),

    ]
    return middleware

def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )
    init_routers(app=app_)
    init_listeners(app=app_)
    return app_
app = create_app()
