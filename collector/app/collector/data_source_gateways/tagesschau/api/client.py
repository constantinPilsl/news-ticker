import logging
from typing import Union

import requests

from collector.data_source_gateways.tagesschau.api.resources import (
    endpoints,
    url,
)


class Client:
    def create_session(self):
        s = requests.Session()
        s.headers.update({"Content-Type": "application/json"})

        return s

    def get_news(
        self,
        session: Union[requests.Session, None] = None,
        url: str = url,
        endpoint: str = endpoints["news"],
    ) -> dict:
        logging.info("tagesschau API - GET request to news endpoint")
        if not session:
            with self.create_session() as session:
                logging.debug(url + endpoint)
                response = session.get(url + endpoint)

                # TODO:  Add better try and sleep + retry
                if response.status_code == 200:
                    logging.info("Received status code 200")
                    return response.json()
                else:
                    raise Exception(
                        f"""Error
Expected status code:  200
Request made to:  {url + endpoint}
Got status code:  {response.status_code}
Response text:
{response.text}
"""
                    )
