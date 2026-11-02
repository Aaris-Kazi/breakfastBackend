from functools import lru_cache
from os import getenv
from dotenv import load_dotenv

class Configurations:

    load_dotenv()
    def __init__(self):
        self.OTEL_SERVICE_NAME = getenv('OTEL_SERVICE_NAME')
        self.OTEL_EXPORTER_OTLP_ENDPOINT = getenv('OTEL_EXPORTER_OTLP_ENDPOINT')
        self.OTEL_RESOURCE_ATTRIBUTES = getenv('OTEL_RESOURCE_ATTRIBUTES')

    @lru_cache
    @staticmethod
    def get_configurations(name, default:str = None) -> str:
        if default is None:
            return getenv(name, "")
        else:
            return getenv(name, default)

        
