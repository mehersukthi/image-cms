import logging
from app.core.server import AppServer

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    server = AppServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()