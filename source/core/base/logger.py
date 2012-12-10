import logging
import sys

FORMAT = "%(asctime)s %(filename)s [%(levelname)s] %(message)s"
DATEFMT = "%H:%M:%S"

def config_root(level=logging.INFO,
                threshold=logging.WARNING,
                format=FORMAT,
                datefmt=DATEFMT):
    root = logging.getLogger()
    root.setLevel(level)
    formatter = logging.Formatter(format, datefmt)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(level)
    stdout_handler.setFormatter(logging.Formatter(format, datefmt))
    root.addHandler(stdout_handler)

    #stderr_handler = logging.StreamHandler(sys.stderr)
    #stderr_handler.setLevel(logging.ERROR)
    #stderr_handler.setFormatter(logging.Formatter(format, datefmt))
    #root.addHandler(stderr_handler)
