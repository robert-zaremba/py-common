import logging
import sys, traceback

try:
    import config
except:
    config = None

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'black'    : "\033[30m",
    #'black_bg': "\033[40",     - analogous as foreground colors, but starting from 40 (red: 41...)
    'red'      : "\033[31m",
    'green'    : "\033[32m",
    'yellow'   : "\033[33m",
    'blue'     : "\033[34m",
    'magenta'  : "\033[35m",
    'cyan'     : "\033[36m",
    'white'    : "\033[37m",
    'bold'     : "\033[1m",

    'fatal'     : "\033[31;1m"  # red bold
}
RESET_SEQ = "\033[0m"
CHECK = u'\t{}\u2714{}'.format(COLORS['green'], RESET_SEQ)
logging.Logger.CHECK = CHECK

class Formatter(logging.Formatter):
    format_str = "%(levelname)1.1s %(name)s: %(module)s.%(funcName)s:%(lineno)d --- %(message)s"
    format_str_color = "%(levelname)1.1s %(name)s: %(module)s..%(funcName)s:%(lineno)d ---{reset} %(message)s".format(reset=RESET_SEQ)

    def __init__(self, colored=False, prefix=""):
        if colored:
            logging.Formatter.__init__(self, prefix+self.format_str_color)
            self.format = self.format_color
        else:
            logging.Formatter.__init__(self, prefix+self.format_str)

    def format_color(self, record):
        levelno = record.levelno
        if( levelno >= 50 ): # CRITICAL / FATAL
            color = COLORS['fatal']
        elif( levelno >= 40 ): # ERROR
            color = COLORS['red']
        elif( levelno >= 30 ): # WARNING
            color = COLORS['yellow']
        elif( levelno >= 20 ): # INFO
            color = COLORS['magenta']
        elif( levelno >= 10 ): # DEBUG
            color = ''  # no color

        return color + logging.Formatter.format(self, record)

    def extract_lines(self, iterable):
        for i in iterable:
            for line in i[:-1].split('\n'):
                yield line

    def formatException(self, ei):
        """
        Format and return the specified exception information as a string.
        """
        lines = traceback.format_exception(ei[0], ei[1], ei[2])
        if hasattr(ei[1], 'msg'):
            lines[-1] = lines[-1][:-1] + '  {}\n'.format(ei[1].msg)
        return 'TRACE '+'\nTRACE '.join(self.extract_lines(lines))


_name = getattr(config, 'name', 'root') or 'root'
_debug = getattr(config, 'debug', False)
_log_colored = getattr(config, 'log_colored', False)

def make_logger(name, level=None, debug=_debug, colored=_log_colored, propagate=0, force=False):
    if level is None:
        level = logging.DEBUG if debug else logging.INFO
    logger = logging.getLogger(name)
    if not logger.handlers or force:
        logger.handlers = []
        handler = logging.StreamHandler()
        #handler_t.setFormatter(logging.Formatter("%(levelname)1.1s %(module)s.%(funcName)s:%(lineno)d --- %(message)s"))
        handler.setFormatter(Formatter(colored=colored))
        logger.addHandler(handler)
        logger.propagate = propagate
    logger.setLevel(level)
    return logger


# if hasattr(sys, '_called_from_test'):    # Check if called from py.test
#     log = make_logger(_name+'_tests', _debug=_debug)
# else:
#     log = make_logger(_name, debug=_debug)

loggerRoot = make_logger(None, logging.WARNING if _debug else logging.INFO, debug=_debug)
