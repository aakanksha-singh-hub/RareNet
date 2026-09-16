import os
import sys
import logging
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

from app.services.cyborg_service import cyborg_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reset_db():
    logger.info("Resetting CyborgDB Indices...")
    try:
        indices = cyborg_service.client.list_indexes()
        logger.info(f"Found indices: {indices}")

        for index_name in indices:
            if index_name.startswith("rarenet_"):
                institution = index_name.removeprefix("rarenet_")
                try:
                    index = cyborg_service.client.load_index(
                        index_name, index_key=cyborg_service.get_index_key(institution)
                    )
                    if hasattr(index, 'delete'):
                        index.delete()
                        logger.info(f"Deleted {index_name}")
                    else:
                        logger.warning(
                            f"Index object for {index_name} has no delete method."
                        )
                except Exception as e:
                    logger.error(f"Failed to load/delete {index_name}: {e}")

        logger.info("Reset complete.")
    except Exception as e:
        logger.error(f"Failed to reset DB: {e}")


if __name__ == "__main__":
    reset_db()
