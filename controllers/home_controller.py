from fastapi import APIRouter
from fastapi.responses import  RedirectResponse


home_router = APIRouter()

@home_router.get("/", response_class=RedirectResponse)
def home():
    return RedirectResponse('/activities', status_code=302)