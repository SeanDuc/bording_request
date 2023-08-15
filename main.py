from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from controllers.activities_controller import activities_router
from controllers.home_controller import home_router
from typing import Annotated
from middleware.auth import get_current_username
import bcrypt
import sqlite3



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.middleware("http")
async def auth(request: Request, call_next):
    response = HTMLResponse()
    response.status_code = 401
    response.headers["WWW-Authenticate"] = "Basic"
    con = sqlite3.connect('activity_data.sqlite')
    cur = con.cursor()
    
    #con.execute(''' CREATE TABLE users(id integer primary key, username text, password text);''')
    
    #password = "password"
    #encoded = password.encode('utf-8')
    #salt = bcrypt.gensalt()
    #hash = bcrypt.hashpw(encoded, salt)
    #cur.execute("insert into users values (null, ?, ?)", ("username", hash))

    con.commit()

    security = HTTPBasic()
    try:
        credentials = await security.__call__(request)
        if credentials:
            input_username = credentials.username
            input_password = credentials.password.encode('utf-8')
            hashed_password_list = cur.execute("select password from users where username = ?", (input_username, )).fetchall()
            if len(hashed_password_list) > 0:
                hashed_password = hashed_password_list[0][0]
                if bcrypt.checkpw(input_password, hashed_password):
                    response = await call_next(request)
    except HTTPException as exc:
        print(exc)
    return response
#    return {"username": username}

app.include_router(home_router)
app.include_router(activities_router)

