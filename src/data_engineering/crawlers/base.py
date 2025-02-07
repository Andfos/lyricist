import time
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
import os
from src.settings import settings
#from dotenv import load_dotenv

#load_dotenv()


class BaseCrawler(ABC):
    #model: type[NoSQLBaseDocument]

    @abstractmethod
    def extract(self, link: str, **kwargs) -> None:
        pass


class LyricsCrawler(BaseCrawler):

    def __init__(self):
        self.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def _query_stands4_lyrics_api(self, link: str) -> requests.Response:
        params = {
            "uid": settings.STANDS4_ID,
            "tokenid": settings.STANDS4_TOKEN,
            "term": "smells like teen spirit",
            "artist": "nirvana",
            "format": "json"
        }

        response = requests.get(url=link, params=params, headers=self.headers)

        return response

    def _get_lyrics(self, response: requests.Response) -> str:

        try:
            song_link = response.json()["result"][0]["song-link"]
        except KeyError:
            print("Error: Song not found")
            return None

        response = requests.get(url=song_link, headers=self.headers)
        if not response.status_code == 200:
            print(f"Error: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        # Find the lyrics inside the <pre> tag
        lyrics = soup.find("pre", id="lyric-body-text")
        lyrics_cleaned = lyrics.text.strip()

        return lyrics_cleaned


    def extract(self, link: str = "https://www.stands4.com/services/v2/lyrics.php", **kwargs) -> None:
        response = self._query_stands4_lyrics_api(link=link)

        if not response.status_code == 200:
            print(f"Error: {response.status_code}")
        
        lyrics = self._get_lyrics(response=response)
        print(lyrics)







if __name__ == '__main__':

    crawler = LyricsCrawler()
    crawler.extract()

