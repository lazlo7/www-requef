from www_requef.spotify.persistent_token_storage import PersistentTokenStorage
from www_requef.spotify.client import SpotifyClient
from www_requef.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, APP_STORAGE_PATH


token_storage = PersistentTokenStorage(APP_STORAGE_PATH)
client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, token_storage)


def get_client() -> SpotifyClient:
    return client
