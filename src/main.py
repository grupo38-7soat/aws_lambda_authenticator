import sys
from loguru import logger

from services.expose_api_service import ApiService

logger.remove(0)
logger.add(sys.stdout)
logger.info('start aplication')

if __name__ == '__main__':
    ApiService().run()
