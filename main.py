from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controllers.activities_controller import activities_router
from controllers.home_controller import home_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(home_router)
app.include_router(activities_router)

