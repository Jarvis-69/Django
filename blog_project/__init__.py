# import os
# import logging

# logger = logging.getLogger(__name__)

# ENV = os.getenv('DJANGO_ENV', 'development')

# if ENV == 'production':
#     from .production import *
#     print("Using production settings")
#     logger.info("Using production settings")
# else:
#     from .development import *
#     print("Using development settings")
#     logger.info("Using development settings")