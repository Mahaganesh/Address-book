import os

env = os.getenv('ADB', 'dev')
if env == 'local':
    from .local_config import Configuration
if env == 'dev':
    from .dev_config import Configuration