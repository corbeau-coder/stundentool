import os
from loguru import logger
from typing import Tuple

def remove_db_file(path) -> Tuple[bool, Exception]:
    logger.debug("IO module deleting db at {path}")
    try:
        os.remove(path)
    except Exception as e:
        logger.debug("FAILED: {e}")
        return False,(e)
    else:
        logger.debug("DONE")
        return True,None