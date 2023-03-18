## Installed ##
from fastapi import FastAPI, Depends
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError


# Package ##
from .core.settings import api_settings as settings
from .middlewares import request_handler, validation_exception_handler, debug_exception_handler
from .routers import usermangement, interface, templete, notification


origins = ["*"]

app = FastAPI(
    docs_url=settings.docs_url,
    redoc_url=settings.redocs_url,
    title=settings.title,
    description=settings.description,
    version=settings.version,
    openapi_url=settings.openapi_url,
    autoopen=False
    )

''' Middleware '''
app.middleware("http")(request_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

""" Functions that run as something is processed """
app.exception_handler(RequestValidationError)(validation_exception_handler)
app.exception_handler(Exception)(debug_exception_handler)


app.include_router(usermangement.router, tags=["Usermanegement"])
app.include_router(interface.router, tags=["Ethernet_Interface"])
app.include_router(templete.router, tags=["Templete"])
app.include_router(notification.router, tags=["Notification"])


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
    
