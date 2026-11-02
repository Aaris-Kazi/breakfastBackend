from enum import Enum
from utils import Configurations
from .AppEnums import AppEnums


class AppConstants(Enum):
    DEFAULT_DELIVERY_FEE = Configurations.get_configurations("DEFAULT_DELIVERY_FEE", AppEnums.DEFAULT_DELIVERY_FEE)
    HOSTNAME = Configurations.get_configurations("HOST", "localhost")
    DB_NAME = Configurations.get_configurations("DELIVERY_DATABASE", "deliveryApp")
    USERNAME = Configurations.get_configurations("USERNAME", "aaris")
    PASSWORD = Configurations.get_configurations("PASSWORD", "12345")
    POOL_SIZE = Configurations.get_configurations("POOL_SIZE", 50)
    ACCESS_TOKEN_HOURS = Configurations.get_configurations("TOKEN_HOURS", 24)
    REFRESH_TOKEN_DAYS = Configurations.get_configurations("TOKEN_DAYS", 7)
    SECRETS = Configurations.get_configurations("SECRETS", "thisisthesecret while building the application")