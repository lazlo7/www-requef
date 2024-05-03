from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from random import choice

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.exception_handler(404)
async def custom_404_handler(request: Request, _):
    comments = [
        "uhhhm, you sure this what you looking for?",
        "this might be a dead end",
        "you're lost, aren't you?",
        "you might want to turn back",
        "nothing's here, nobody's here"
    ]
    return templates.TemplateResponse("404.html", {"request": request, "comment": choice(comments)})

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
