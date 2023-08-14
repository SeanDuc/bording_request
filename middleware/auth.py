from fastapi import FastAPI, Request, APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from mako.lookup import TemplateLookup
from bored.models.activity import Activity
from mako.template import Template
from typing import Annotated
import secrets
import requests
import sqlite3

security = HTTPBasic()

async def get_current_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"username"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"password"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

