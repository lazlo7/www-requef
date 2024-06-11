from string import ascii_letters, digits
from random import choices
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


class SpotifyController:
    __router = APIRouter(prefix="/spotify")


    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, templates: Jinja2Templates):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__redirect_uri = redirect_uri
        self.__templates = templates
        self.__authorized = False
        self.__state = ""


    @staticmethod
    def __generate_random_state() -> str:
        chars = ascii_letters + digits
        return "".join(choices(chars, k=16))


    def registerRoutes(self, app: FastAPI):
        app.include_router(self.__router)


    @__router.get("/login")
    async def login(self, request: Request):
        self.__state = self.__generate_random_state()
        scope = "user-read-currently-playing";
        return RedirectResponse(f"https://accounts.spotify.com/authorize?response_type=code&
                                client_id={self.__client_id}&
                                scope={scope}&
                                redirect_uri={self.__redirect_uri}&
                                state={self.__state}")


    @__router.get("/callback")
    async def callback(self, request: Request, code: str | None = None, state: str | None = None):
        if state is None or state != self.__state:
            return self.__templates.TemplateResponse("spotify/login_rejected.html",
                                                     {"request": request},
                                                     status_code=403)
        
        if code is None:
            return self.__templates.TemplateResponse("spotify/login_rejected.html",
                                                     {"request": request},
                                                     status_code=403)
        
        self.__authorized = True
        


    def get_current_track(self) -> tuple[str, str]:
        pass