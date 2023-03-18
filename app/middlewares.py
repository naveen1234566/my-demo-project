
## Native ##
import json
import traceback

# # Installed # #
from fastapi import Request, status, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

""" Costomize the traceback error validation"""
async def debug_exception_handler(request: Request, exc: Exception):
    return Response(
        content="".join(
            traceback.format_exception(
                etype=type(exc), value=exc, tb=exc.__traceback__
            )
        )
    )

""" Costomize the pydantic error validation"""
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    modified_details = []
    for error in details:
        modified_details.append(
            {
                "field": error["loc"][1],
                "msg": error["msg"]
            }
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )


""" Costomize the response error validation"""
async def request_handler(request: Request, call_next):
    response = await call_next(request)
    response_body = b''
    resData = {}
    # Swagger and Redoc Return statement
    if request.url.path == '/api/v1/docs' or request.url.path == '/api/v1/openapi.json':
        return response

    if request.url.path == '/api/v1/redoc':
        return response
    #response body
    if response.body_iterator:
        async for chunk in response.body_iterator:
            response_body += chunk

        convertResBody = response_body.decode('utf-8')
        resData = json.loads(convertResBody)

        if resData.get("detail") is None and type(resData) == dict:
            return JSONResponse(status_code=response.status_code, content=resData)
    
        if resData["detail"] is not None and type(resData["detail"]) == str:
            detail = [
                    {
                        "field":"API",
                        "msg": resData["detail"]
                    }
                ]
            return JSONResponse(status_code=response.status_code, content=jsonable_encoder({"detail": detail}))
        else:
            return JSONResponse(status_code=response.status_code, content=resData)