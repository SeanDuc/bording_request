from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from mako.lookup import TemplateLookup
from bored.models.activity import Activity
from mako.template import Template
import requests
import sqlite3


activities_router = APIRouter(prefix="/activities")
views = TemplateLookup(directories=['views', 'views/activities'])

def get_db():
    return sqlite3.connect('activity_data.sqlite')


@activities_router.get("/", response_class=HTMLResponse)
def home(request: Request, con = Depends(get_db)):
    cur = con.cursor()
    cursor = cur.execute("select key, activity, type from activ").fetchall()
    results = []
    for row in cursor:
        activity = Activity(row)
        results.append(activity)

    templ = views.get_template("/activities/index.html")
    html = templ.render(activities = reversed(results))
    return HTMLResponse(html)

@activities_router.post("/", response_class=RedirectResponse)
def insert(request: Request, con = Depends(get_db)):
    cur = con.cursor()
    response = requests.get("https://www.boredapi.com/api/activity")
    response_json = response.json()
    #print(response_json["activity"])
    #sql.execute(''' CREATE TABLE activ(FIND INT key, activity text, type text);''')

    cur.execute("insert into activ values (?, ?, ?)", (response_json["key"], response_json["activity"], response_json["type"]))
    con.commit()

    return RedirectResponse('/activities', status_code=302)

@activities_router.get("/{key}", response_class=HTMLResponse)
def details(key: int, request: Request, con = Depends(get_db)):
    cur = con.cursor()
    cursor = cur.execute("select * from activ where key = ?", (key,)).fetchall()
    templ = views.get_template("/activities/details.html")
    activity = Activity(cursor[0])
    html = templ.render(activity = activity)
    return HTMLResponse(html)




    