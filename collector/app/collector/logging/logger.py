import logging
import uuid

session_id = str(uuid.uuid4())

logging.basicConfig(
    format="\"{session_id}\"\t|\t%(asctime)s\t|\t[%(levelname)s]\t|\t%(message)s".format(
        session_id=session_id
    ),
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %I:%M:%S",
    # filename="logs/application_logs.log",
    # filemode="a",
)

logging.info("Start application")

logger = logging.getLogger("collector")
