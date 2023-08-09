from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from bored.models.activity import Activity
import requests
import sqlite3

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    response = requests.get("https://www.boredapi.com/api/activity")
    response_json = response.json()
    #print(response_json["activity"])

    act = Activity(response_json["activity"], 
                 response_json["type"], 
                 response_json["participants"], 
                 response_json["price"], 
                 response_json["key"], 
                 response_json["accessibility"])

    #print(act.__dict__)


    connection = sqlite3.connect('activity_data.db')
    cur = connection.cursor()
    #sql.execute(''' CREATE TABLE activ(FIND INT key, activity text, type text);''')

    cur.execute("insert into activ values (?, ?, ?)", (response_json["key"], response_json["activity"], response_json["type"]))
    connection.commit()

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
            {rows}
        </body>
    </html>
    """.format(rows = data)