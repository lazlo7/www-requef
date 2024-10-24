from www_requef.dependencies import get_templates
from www_requef.config import SPOTIFY_ENABLED, CV_URL
from random import choice
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
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
    return t.TemplateResponse("404.html", 
                              {"request": req, "comment": choice(comments)},
                              status_code=404)


@app.get("/")
async def index(req: Request,
               t: Jinja2Templates = Depends(get_templates)):
    return t.TemplateResponse("index.html", {"request": req})


@app.get("/cv")
async def cv():
    if not CV_URL:
        raise HTTPException(status_code=404, detail="CV not available")
    return RedirectResponse(CV_URL)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("www_requef.main:app", host="0.0.0.0", port=8000, reload=True)
