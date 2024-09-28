from dotenv import load_dotenv
import os

load_dotenv('application.env')

class Config(object):
    @staticmethod
    def get(name: str) -> str:
        return os.getenv(name)