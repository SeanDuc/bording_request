from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from bored.models.activity import Activity
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
def home():
    connection = sqlite3.connect('activity_data.db')
    cur = connection.cursor()
    cursor = connection.execute("select * from activ")
    data = ""
    for row in cursor:
        data += row[1] + "<br/>"
    

    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
            <form action="/act" method="POST">
                <input type="submit" value="add activity">	
            </form>
            {rows}
        </body>
    </html>
    """.format(rows = data)