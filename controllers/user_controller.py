from fastapi import Request, APIRouter, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from mako.lookup import TemplateLookup
from fastapi import Response
import bcrypt
import sqlite3

user_router = APIRouter(prefix="/user")
views = TemplateLookup(directories=['views', 'views/user'])



#main branch
@user_router.get("/", response_class=RedirectResponse)
def user_redirect(request: Request):
    
    if request.cookies.get("session_id") is not None:
        return RedirectResponse('/user/logout', status_code=302)
    else:
        return RedirectResponse('/user/login', status_code=302)

#login
@user_router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    templ = views.get_template("/user/login.html")
    html = templ.render()
    return HTMLResponse(html)

@user_router.post("/login", response_class=RedirectResponse)
def login_post(request: Request, username: str = Form(), password: str = Form()):
    correct_login = False
    con = sqlite3.connect('activity_data.sqlite')
    cur = con.cursor()
    input_password = password.encode('utf-8')
    hashed_password_list = cur.execute("select password from users where username = ?", (username, )).fetchall()
    if len(hashed_password_list) > 0:
        hashed_password = hashed_password_list[0][0]
        if bcrypt.checkpw(input_password, hashed_password):
            correct_login = True
    if correct_login:
        response = RedirectResponse('/activities', status_code=302)
        response.set_cookie(key="session_id", value=username)
    else:
        print("incorrect username or password")
        response = RedirectResponse('/user/login', status_code=302)
    return response




#logout
@user_router.get("/logout", response_class=HTMLResponse)
def logout_get(request: Request, response: Response):
    templ = views.get_template("/user/logout.html")
    html = templ.render()
    return HTMLResponse(html)

@user_router.post("/logout", response_class=RedirectResponse)
def logout_post(request: Request):
    response = RedirectResponse('/user/login', status_code=302)
    response.delete_cookie(key="session_id")
    return response


#signin
@user_router.get("/signin", response_class=HTMLResponse)
def signin_get(request: Request, response: Response):
    templ = views.get_template("/user/signin.html")
    html = templ.render()
    return HTMLResponse(html)

@user_router.post("/signin", response_class=RedirectResponse)
def signin_post(request: Request, username: str = Form(), password: str = Form()):
    con = sqlite3.connect('activity_data.sqlite')
    cur = con.cursor()
    response = RedirectResponse('/activities', status_code=302)
    if len(password) >= 8:
        encoded_password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(encoded_password, salt)
        cur.execute("insert into users values (null, ?, ?)", (username, hash))
        con.commit()
        response.set_cookie(key="session_id", value=username)
    else: 
        print("password too short")
        response = RedirectResponse('/user/signin', status_code=302)
    return response
