import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from colorama import init
from colorama import Fore, Style


init(autoreset=True)

DEFAULT_LOG_PATH = Path("logs")

LINE_WIDTH = 100
CHECK_MARK = "\N{check mark}"
X = "x"


def check_directory_exists(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)


def color_me(msg, color):
    """
    Sets color values for colorama
    """

    colors = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "white": Fore.WHITE,
        "black": Fore.BLACK,
        "blue": Fore.BLUE,
        "yellow": Fore.YELLOW,
    }
    assert color in colors, f"'{color}' is not supported"
    return colors[color] + msg + Style.RESET_ALL


def make_logger():
    """
    Return a logger instance.
    """
    _logger = logging.getLogger(__name__)

    print_message_format = "%(message)s"
    print_formatter = logging.Formatter(print_message_format, datefmt="%H:%M:%S")

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(print_formatter)

    Path(DEFAULT_LOG_PATH).mkdir(parents=True, exist_ok=True)

    log_message_format = "%(asctime)s | %(message)s"
    log_formatter = logging.Formatter(log_message_format, datefmt="%H:%M:%S")
    log_path = DEFAULT_LOG_PATH.joinpath("dbtbt.log")
    fh = TimedRotatingFileHandler(
        filename=log_path, when="d", interval=1, backupCount=7
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(log_formatter)

    _logger.addHandler(ch)
    _logger.addHandler(fh)
    _logger.setLevel(logging.INFO)

    return _logger


logger = make_logger()
