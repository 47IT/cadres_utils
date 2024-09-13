import logging


def init_logger(debug_level = logging.DEBUG):
    logging.basicConfig(
        level=debug_level,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
