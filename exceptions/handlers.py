from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    def http_exc_handler(request: Request, exc: HTTPException):
        return ORJSONResponse(
            status_code=exc.status_code,
            content={
                "status_code": exc.status_code,
                "message": exc.detail
            }
        )

    @app.exception_handler(RequestValidationError)
    def request_validation_err_handler(request: Request, exc: RequestValidationError):
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "Validation failed",
                "errors": [
                    {
                        "location": err["loc"],
                        "message": err["msg"], 
                        "input_value": err["input"]
                    } for err in exc.errors()
                ]
            }
        )