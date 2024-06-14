from starlette.config import Config

config = Config(".env")

APP_WEB_PORT = config("APP_WEB_PORT", cast=int, default=8000)

APP_STORAGE_PATH = config("APP_STORAGE_PATH", cast=str, default="")
SPOTIFY_CLIENT_ID = config("SPOTIFY_CLIENT_ID", cast=str, default="")
SPOTIFY_CLIENT_SECRET = config("SPOTIFY_CLIENT_SECRET", cast=str, default="")
SPOTIFY_REDIRECT_URI = config("SPOTIFY_REDIRECT_URI", cast=str, default="")

SPOTIFY_ENABLED = all([APP_STORAGE_PATH, 
                       SPOTIFY_CLIENT_ID, 
                       SPOTIFY_CLIENT_SECRET, 
                       SPOTIFY_REDIRECT_URI])

print(SPOTIFY_REDIRECT_URI)