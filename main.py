from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from mako.lookup import TemplateLookup
from bored.models.activity import Activity
from mako.template import Template
import requests
import sqlite3

app = FastAPI()

@app.post("/act", response_class=RedirectResponse)
def insert():
    response = requests.get("https://www.boredapi.com/api/activity")
    response_json = response.json()
    #print(response_json["activity"])

    connection = sqlite3.connect('activity_data.db')
    cur = connection.cursor()
    #sql.execute(''' CREATE TABLE activ(FIND INT key, activity text, type text);''')

    cur.execute("insert into activ values (?, ?, ?)", (response_json["key"], response_json["activity"], response_json["type"]))
    connection.commit()

    return RedirectResponse('/', status_code=302)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    connection = sqlite3.connect('activity_data.db')
    cur = connection.cursor()
    cursor = cur.execute("select * from activ").fetchall()
    views = TemplateLookup(directories=['views'])
    templ = views.get_template("/home/index.html")
    #for row in cursor:
    #    print(row[1])
    return HTMLResponse(templ.render(activities = cursor))
    