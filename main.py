from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from controllers.activities_controller import activities_router
from controllers.home_controller import home_router
from controllers.user_controller import user_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.middleware("http")
async def auth(request: Request, call_next):
    
    
    
    #con.execute(''' CREATE TABLE users(id integer primary key, username text, password text);''')
    

    if request['path'] == "/activities/" and request.method == "POST" :
        response = RedirectResponse('/user/login')
        response.status_code = 302
        if request.cookies.get("session_id") is not None:
            response = await call_next(request)
    else:
        response = await call_next(request)

    return response
#    return {"username": username}

app.include_router(home_router)
app.include_router(activities_router)
app.include_router(user_router)

