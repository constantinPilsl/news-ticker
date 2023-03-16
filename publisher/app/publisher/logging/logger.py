import logging
import os
import uuid

session_id = str(uuid.uuid4())
current_directory = os.getcwd()

print(current_directory)

logging.basicConfig(
    format="\"{session_id}\"\t|\t%(asctime)s\t|\t[%(levelname)s]\t|\t%(message)s".format(
        session_id=session_id
    ),
    level=logging.INFO,
    datefmt="%Y-%m-%d %I:%M:%S",
    # filename="logs/application_logs.log",
    # filemode="a",
)

logging.info("Start application")

logger = logging.getLogger("publisher")
