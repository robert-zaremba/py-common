from src import logger
from io import BytesIO


def make_sequence(log, msg=""):
    log.debug('debug')
    log.warning('warning')
    log.info('info')
    log.error('error: {0}'.format(msg))
    log.fatal('fatal')
    try:
        raise RuntimeError("cos sie spieprzylo")
    except Exception:
        log.exception('exception')


def test_logger():
    #print dir(logger)
    #make_sequence(logger.logger)

    make_sequence(logger.make_logger("testowy logger", debug=True, colored=True))
    make_sequence(logger.make_logger("logger_nocolor", debug=True, colored=False), False)
