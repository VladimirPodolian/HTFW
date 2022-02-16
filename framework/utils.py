import logging


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)s]%(message)s',
)


def log(msg):
    return logging.info(msg)


def cut_log_data(data: str, length=50) -> str:
    """
    Cut given data for reducing log length

    :param data: original data ~ 'very long string for typing. string endless continues'
    :param length: length to cut given data ~ 20
    :return: edited data ~ 'Type text: "very long string for >>> 36 characters"'
    """
    return f'{data[:length]} >>> {len(data[length:])} characters' if len(data) > length else data
