from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from controllers.activities_controller import activities_router
from controllers.home_controller import home_router
from typing import Annotated
from middleware.auth import get_current_username
import time

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.middleware("http")
async def auth(request: Request, call_next):
    response = HTMLResponse()
    response.status_code = 401
    response.headers["WWW-Authenticate"] = "Basic"

    security = HTTPBasic()
    try:
        credentials = await security.__call__(request)
        if credentials:
            if credentials.username == "username" and credentials.password == "password":
                response = await call_next(request)
    except HTTPException as exc:
        print(exc)
    return response
#    return {"username": username}

app.include_router(home_router)
app.include_router(activities_router)

