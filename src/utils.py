import random
import string


def random_string(length=(10, 30), letters=True, numbers=True):
    """
    Return random string

    :param length: length to randint from
    :param letters: attach letter in output
    :param numbers: attach number in output
    :return: string object ~ 'asdfg53423qfe'
    """
    output = ''
    if letters:
        output += string.ascii_lowercase
    if numbers:
        output += string.digits
    return ''.join(random.choice(output) for _ in range(random.randint(length[0], length[1])))


def parse_echelon_data(echelon_data):
    """
    Parse echelon data for request
    page_size/page_start/page_stop variables used for api requests

    :param echelon_data: dict object. One from `echelons_data`
    :return: tuple(page_size, page_start, page_stop, page_url)
    """
    places, page_url = echelon_data['places'], echelon_data['url']
    page_size, page_start, page_stop = places.stop - places.start, places.start, places.stop - 1
    return page_size, page_start, page_stop, page_url
