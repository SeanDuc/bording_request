from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from mako.lookup import TemplateLookup
from bored.models.activity import Activity
from mako.template import Template
import requests
import sqlite3


activities_router = APIRouter(prefix="/activities")
views = TemplateLookup(directories=['views', 'views/home'])

@activities_router.get("/", response_class=HTMLResponse)
def home(request: Request):
    connection = sqlite3.connect('activity_data.db')
    cur = connection.cursor()
    cursor = cur.execute("select * from activ").fetchall()
    templ = views.get_template("/home/index.html")
    html = templ.render(activities = cursor)
    print(html)
    return HTMLResponse(html)

@activities_router.post("/", response_class=RedirectResponse)
def insert():
    response = requests.get("https://www.boredapi.com/api/activity")
    response_json = response.json()
    #print(response_json["activity"])

    connection = sqlite3.connect('activity_data.db')
    cur = connection.cursor()
    #sql.execute(''' CREATE TABLE activ(FIND INT key, activity text, type text);''')

    cur.execute("insert into activ values (?, ?, ?)", (response_json["key"], response_json["activity"], response_json["type"]))
    connection.commit()

    return RedirectResponse('/activities', status_code=302)



    