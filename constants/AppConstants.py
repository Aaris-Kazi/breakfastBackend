from enum import Enum
from utils import Configurations
from .AppEnums import AppEnums


class AppConstants(Enum):
    DEFAULT_DELIVERY_FEE = Configurations.get_configurations("DEFAULT_DELIVERY_FEE", AppEnums.DEFAULT_DELIVERY_FEE)
    HOSTNAME = Configurations.get_configurations("HOST")
    DB_NAME = Configurations.get_configurations("DELIVERY_DATABASE")
    USERNAME = Configurations.get_configurations("USERNAME")
    PASSWORD = Configurations.get_configurations("PASSWORD")
    POOL_SIZE = Configurations.get_configurations("POOL_SIZE")
    ACCESS_TOKEN_HOURS = Configurations.get_configurations("TOKEN_HOURS", 24)
    REFRESH_TOKEN_DAYS = Configurations.get_configurations("TOKEN_DAYS", 7)
    SECRETS = Configurations.get_configurations("SECRETS")