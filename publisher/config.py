from typing import Any, Literal, Union

import yaml
from pydantic import BaseModel

from publisher.logging.logger import logger, session_id


class Config(BaseModel):
    session_id: str = session_id
    logger: Any = logger
    collector: Union[dict, None]
    publisher: Union[dict, None]
    env: Union[Literal["prd", "dev"], None]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_resources()
        self.log_config_initialization()

    def set_resources(self):
        with open("publisher/resources/resources.yml", "r") as stream:
            resources = yaml.safe_load(stream)
        self.collector = resources["collector"]
        self.publisher = resources["publisher"]
        self.env = resources["env"]

    def log_config_initialization(self):
        self.logger.info("Config initialized")
        self.logger.info(self.dict())
