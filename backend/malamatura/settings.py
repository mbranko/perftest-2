import logging
import os

logger = logging.getLogger(__name__)

if 'DJANGO_SETTINGS' in os.environ:
    cfg = os.environ['DJANGO_SETTINGS']
    if cfg == "dev":
        logger.info('Configuration: dev')
        from malamatura.app_settings.dev import *
    elif cfg == "prod":
        logger.info('Configuration: prod')
        from malamatura.app_settings.prod import *
    else:
        logger.fatal('Unknown configuration')
else:
    logger.info('Configuration not set, defaulting to: dev')
    from malamatura.app_settings.dev import *
