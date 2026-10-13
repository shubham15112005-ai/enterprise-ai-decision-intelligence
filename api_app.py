from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

from config.settings import (
    APP_NAME,
    APP_VERSION,
    CORS_ORIGINS,
    ENVIRONMENT,
)
from fastapi import Request
from fastapi.responses import JSONResponse

from api.routes import (
    DecisionAPIError,
    router,
)
from utils.logger import configure_logging


print("Shubham Sharma 23051870")


configure_logging()


app = FastAPI(
    title=f"{APP_NAME} API",
    description=(
        "REST API for evidence-based "
        "business decision intelligence."
    ),
    version=APP_VERSION,
)
@app.exception_handler(DecisionAPIError)
async def decision_api_error_handler(
    request: Request,
    exc: DecisionAPIError,
):
    return JSONResponse(
        status_code=exc.status,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "status": exc.status,
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
):
    messages = []

    for error in exc.errors():
        location = ".".join(
            str(item)
            for item in error.get(
                "loc",
                [],
            )
        )

        message = error.get(
            "msg",
            "Invalid request.",
        )

        if location:
            messages.append(
                f"{location}: {message}"
            )
        else:
            messages.append(message)

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "; ".join(messages),
                "status": 422,
            }
        },
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "application": APP_NAME,
        "status": "running",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
    }