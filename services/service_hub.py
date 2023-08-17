from fastapi import FastAPI, Request, APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from mako.lookup import TemplateLookup
from bored.models.activity import Activity
from mako.template import Template
from typing import Annotated, Any
from dotenv import load_dotenv
import os
import openai
import requests
import sqlite3



def get_db():
    return sqlite3.connect('activity_data.sqlite')

def get_all_activities(con = Depends(get_db)):
    cur = con.cursor()
    cursor = cur.execute("select key, activity, type, instructions from activ").fetchall()
    results = []
    for row in cursor:
        activity = Activity(row)
        results.append(activity)
    results = reversed(results)
    return results

def post_activity(con = Depends(get_db)):
    cur = con.cursor()
    response = requests.get("https://www.boredapi.com/api/activity")
    response_json = response.json()
    #con.execute(''' CREATE TABLE activ(FIND INT key, activity text, type text, instructions text);''')
    instructions = generate_instructions(response_json["activity"])
    cur.execute("insert into activ values (?, ?, ?, ?)", (response_json["key"], response_json["activity"], response_json["type"], instructions))
    con.commit()
    return

class GetSpecificActivity:
    #function being called
    def __call__(self, key: int, con = Depends(get_db)):
        cur = con.cursor()
        cursor = cur.execute("select * from activ where key = ?", (key, )).fetchall()
        activity = Activity(cursor[0])
        return activity
    

def generate_instructions(prompt: str):
    load_dotenv()
    openai.api_key = os.getenv("Open_AI_Key")
    prompt = "make instructions on how to " + prompt + " within 100 words"
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=100)
    generated_text = response.choices[0].text
    return generated_text