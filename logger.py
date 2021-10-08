import logging
import coloredlogs
import sys


logger = logging.getLogger('scb')
logger.setLevel(logging.DEBUG)
coloredlogs.DEFAULT_FIELD_STYLES['levelname'] = {"color": "blue"}
coloredlogs.DEFAULT_FIELD_STYLES['asctime'] = {"color": "magenta"}

coloredlogs.DEFAULT_LEVEL_STYLES['debug'] = {"color": "green"}
coloredlogs.DEFAULT_LEVEL_STYLES['info'] = {"color": "cyan"}

ch = logging.StreamHandler(stream=sys.stdout)  # без выбора sys.stdout пайчарм выводит красный текст как в stderr
ch.setLevel(logging.DEBUG)

ch_formatter = coloredlogs.ColoredFormatter(
    u'[%(asctime)s.%(msecs)03d] %(levelname)s: %(message)s (%(filename)s:%(funcName)s:%(lineno)s)',
    datefmt='%Y-%m-%d %H:%M:%S'
)
ch.setFormatter(ch_formatter)

logger.addHandler(ch)
