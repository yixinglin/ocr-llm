import uvicorn
from api import app
from core.config import config


if __name__ == "__main__":
    server_config = config.server
    uvicorn.run(app, host=server_config.host, port=server_config.port)