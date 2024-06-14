from www_requef.spotify.token_storage import TokenStorage
import os
import json


class PersistentTokenStorage(TokenStorage):
    def __init__(self, path: str):
        self.__path = os.path.join(path, "token_storage.json")
        self.__tokens = {}
        self.__load()


    def __load(self):
        try:
            with open(self.__path, "r") as f:
                self.__tokens = json.load(f)
        except FileNotFoundError:
            pass


    def set(self, token: str, value: str):
        self.__tokens[token] = value
        os.makedirs(os.path.dirname(self.__path), exist_ok=True)
        with open(self.__path, "w") as f:
            json.dump(self.__tokens, f)


    def get(self, token: str) -> str | None:
        return self.__tokens.get(token, None)
