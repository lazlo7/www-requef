from abc import ABC, abstractmethod


class TokenStorage(ABC):
    @abstractmethod
    def set(self, token: str, value: str):
        pass


    @abstractmethod
    def get(self, token: str) -> str | None:
        pass