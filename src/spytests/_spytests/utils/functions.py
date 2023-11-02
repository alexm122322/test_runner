import sys


def get_system_info():
    ver_info = ".".join(map(str, sys.version_info[:3]))
    return f'platform {sys.platform} -- Python {ver_info}'


def item_count_str(word: str, count: int):
    return word if count == 1 else f'{word}s'
