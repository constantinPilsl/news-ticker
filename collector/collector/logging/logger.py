import logging
import uuid

session_id = str(uuid.uuid4())

logging.basicConfig(
    format="\"{session_id}\" | %(asctime)s | [%(levelname)s] | %(message)s".format(
        session_id=session_id
    ),
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %I:%M:%S",
    filename="logs/application_logs",
    filemode="a",
)

logging.info("Start application")

logger = logging.getLogger("collector")
