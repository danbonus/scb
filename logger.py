import logging
import verboselogs
import coloredlogs
import sys


logger = verboselogs.VerboseLogger('scb')
logger.setLevel(verboselogs.SPAM)

coloredlogs.DEFAULT_FIELD_STYLES['levelname'] = {"color": "blue"}
coloredlogs.DEFAULT_FIELD_STYLES['asctime'] = {"color": "magenta"}

coloredlogs.DEFAULT_LEVEL_STYLES['debug'] = {"color": "green"}
coloredlogs.DEFAULT_LEVEL_STYLES['info'] = {"color": "cyan"}

stream_handler = logging.StreamHandler(stream=sys.stdout)

ch_formatter = coloredlogs.ColoredFormatter(
    u'[%(asctime)s.%(msecs)03d] %(levelname)s: %(message)s (%(filename)s:%(funcName)s:%(lineno)s)',
    datefmt='%Y-%m-%d %H:%M:%S'
)
stream_handler.setFormatter(ch_formatter)

logger.addHandler(stream_handler)
