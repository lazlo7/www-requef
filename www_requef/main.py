from www_requef.dependencies import get_templates
from www_requef.config import SPOTIFY_ENABLED
from www_requef.spotify.dependencies import get_client as get_spotify_client
from www_requef.spotify.client import SpotifyClient
from random import choice
import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="www_requef/static"), name="static")


if SPOTIFY_ENABLED:
    from www_requef.spotify.routes import router as spotify_router
    app.include_router(spotify_router, prefix="/spotify")
    print("spotify enabled")


@app.exception_handler(404)
async def custom_404_handler(req: Request, _):
    comments = [
        "uhhhm, you sure this what you looking for?",
        "this might be a dead end",
        "you're lost, aren't you?",
        "you might want to turn back",
        "nothing's here, nobody's here"
    ]
    # You can't use dependency injection in exception handlers,
    # so we directly call the function instead.
    t = get_templates()
    return t.TemplateResponse("404.html", {"request": req, "comment": choice(comments)})


@app.get("/")
async def root(req: Request,
               spotify_client: SpotifyClient = Depends(get_spotify_client),
               t: Jinja2Templates = Depends(get_templates)):
    track = spotify_client.get_current_track()
    return t.TemplateResponse("index.html", {"request": req, "track": track})


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("www_requef.main:app", host="0.0.0.0", port=8000, reload=True)
