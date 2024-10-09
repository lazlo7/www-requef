from www_requef.spotify.token_storage import TokenStorage
from www_requef.spotify.utils import cache_result
from string import ascii_letters, digits
from random import choices
from base64 import b64encode
from time import time
import httpx


class SpotifyClient:
    CACHE_INVALIDATION_TIME = 10.0


    def __init__(self, 
                 client_id: str, 
                 client_secret: str, 
                 redirect_uri: str,
                 token_storage: TokenStorage):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__redirect_uri = redirect_uri
        self.__token_storage = token_storage
        self.__state = ""
        self.__access_token = ""
        self.__access_token_timestamp = 0.0
        self.__access_token_expires_in = 0
        self.regenerate_state()


    @property
    def client_id(self) -> str:
        return self.__client_id


    @property
    def authorized(self) -> bool:
        return self.__token_storage.get("refresh_token") is not None


    @property
    def state(self) -> str:
        return self.__state


    def regenerate_state(self):
        chars = ascii_letters + digits
        self.__state = "".join(choices(chars, k=16))


    def __encode_client_auth(self) -> str:
        return b64encode(str.encode(f"{self.__client_id}:{self.__client_secret}")).decode()


    def __update_tokens(self, data: dict[str, str]) -> bool:
        response = httpx.post("https://accounts.spotify.com/api/token",
                              data=data,
                              headers={"Content-Type": "application/x-www-form-urlencoded",
                                       "Authorization": f"Basic {self.__encode_client_auth()}"
                              })
        
        if response.status_code != httpx.codes.OK:
            return False
        
        response_data = response.json()
        self.__access_token = response_data["access_token"]
        self.__access_token_expires_in = response_data["expires_in"]
        self.__access_token_timestamp = time()
        if (refresh_token := response_data.get("refresh_token")) is not None:
            self.__token_storage.set("refresh_token", refresh_token)
        return True


    def request_tokens(self, code: str = "") -> bool:
        if code:
            return self.__update_tokens({
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.__redirect_uri
            })
        
        refresh_token = self.__token_storage.get("refresh_token")
        if refresh_token is None:
            return False
        
        return self.__update_tokens({
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        })


    @cache_result(timeout_s = 10.0)
    async def get_current_track(self) -> dict | None:        
        # Check if access token is expired.
        time_now = time()
        if time_now >= self.__access_token_timestamp + self.__access_token_expires_in:
            if not self.request_tokens():
                return None

        response = httpx.get("https://api.spotify.com/v1/me/player/currently-playing",
                             headers={"Authorization": f"Bearer {self.__access_token}"})
        
        if response.status_code != 200:
            return None
        
        if response.text == "EMPTY RESPONSE":
            return None
        
        response_data = response.json()
        track_id = response_data["item"]["id"]
        track_name = response_data["item"]["name"]
        artist_names = [artist["name"] for artist in response_data["item"]["artists"]]
        album_cover_url = response_data["item"]["album"]["images"][0]["url"]

        result = {
            "track_id": track_id,
            "track_name": track_name, 
            "artist_names": ", ".join(artist_names), 
            "album_cover_url": album_cover_url
        }
        
        return result