import json
import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.BASE_URL = os.getenv("BASE_URL", "/v1/group/")
        self.HOSTS = json.loads(os.getenv("HOSTS", '["node1.example.com", "node2.example.com", "node3.example.com"]'))
        self.RETRY_COUNT = int(os.getenv("RETRY_COUNT", "3"))
        self.WAIT_BETWEEN_RETRIES = int(os.getenv("WAIT_BETWEEN_RETRIES", "10"))
