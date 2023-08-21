from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from mako.lookup import TemplateLookup
from services.service_hub import get_all_activities, post_activity, GetSpecificActivity


activities_router = APIRouter(prefix="/activities")
views = TemplateLookup(directories=['views', 'views/activities'])

#@activities_router.get("/user")
#def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
#    return {"username": credentials.username, "password": credentials.password}

@activities_router.get("/", response_class=HTMLResponse)
def home(request: Request, results = Depends(get_all_activities)):
    templ = views.get_template("/activities/index.html")
    html = templ.render(activities = results)
    return HTMLResponse(html)

@activities_router.post("/", response_class=RedirectResponse)
def insert(request: Request, con = Depends(post_activity)):
    return RedirectResponse('/activities', status_code=302)

@activities_router.get("/{key}", response_class=HTMLResponse)
def details(request: Request, activity= Depends(GetSpecificActivity())):
    templ = views.get_template("/activities/details.html")
    html = templ.render(activity = activity)
    return HTMLResponse(html)




    