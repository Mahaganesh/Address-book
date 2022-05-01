from config.base_config import BaseConfig

class Configuration(BaseConfig):
    DEBUG = True

    DB_URL = 'sqlite:///./address_book.db'
    
