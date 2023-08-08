from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from bored.models.activity import Activity
import requests

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
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

    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
            <div> {activ}</div>
        </body>
    </html>
    """.format(activ = act.activity)