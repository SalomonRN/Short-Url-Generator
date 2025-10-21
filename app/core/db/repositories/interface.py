from abc import ABC, abstractmethod
from models.url import Url


class URLRepository(ABC):
    @abstractmethod
    async def create(self, url: Url):
        pass

    @abstractmethod
    async def get_by_tiny_url(self, tiny_url: str):
        pass
