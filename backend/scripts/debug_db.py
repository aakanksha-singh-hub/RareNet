import os
import sys
import logging
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

from app.services.cyborg_service import cyborg_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def debug_db():
    logger.info("Debugging CyborgDB Indices...")
    try:
        indices = cyborg_service.client.list_indexes()
        logger.info(f"Found indices: {indices}")

        for index_name in indices:
            if index_name.startswith("rarenet_"):
                institution = index_name.removeprefix("rarenet_")
                try:
                    logger.info(f"Inspecting index: {index_name}")
                    index = cyborg_service.client.load_index(
                        index_name, index_key=cyborg_service.get_index_key(institution)
                    )
                    dummy_vector = [0.0] * 384
                    try:
                        results = index.query(dummy_vector, top_k=1, include=["distance"])
                    except TypeError:
                        results = index.query(dummy_vector, top_k=1)
                    logger.info(
                        f"Index {index_name} accessible. Dummy search hits: "
                        f"{len(results) if results else 0}"
                    )
                except Exception as e:
                    logger.error(f"Failed to inspect {index_name}: {e}")

        logger.info("Debug complete.")
    except Exception as e:
        logger.error(f"Failed to debug DB: {e}")


if __name__ == "__main__":
    debug_db()
