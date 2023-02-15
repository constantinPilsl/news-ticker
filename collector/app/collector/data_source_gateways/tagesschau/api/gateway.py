import logging
from typing import Union

import requests


class TagesschauApiGateway:
    def __init__(self):
        self.source: str = "tagesschau"
        self.base_url: str = "https://www.tagesschau.de/api2"
        self.session: Union[requests.Session, None] = self._create_session()

    def _create_session(self):
        session = requests.Session()
        session.headers.update({"Content-Type": "application/json"})
        return session

    def _set_session(self):
        self.session = self._create_session()

    def _close_session(self):
        self.session.close()
        self.session = None

    def get_news(self) -> dict:
        logging.info("tagesschau API - GET request to news endpoint")
        if self.session is None:
            self._set_session()

        url = f"{self.base_url}/news"
        response = self.session.get(url)
        # TODO:  Add better try and sleep + retry
        if response.status_code == 200:
            logging.info(f"Received status code {response.status_code}")
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}")
