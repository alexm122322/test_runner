import os


class FileNotExistException(Exception):
    pass


class FileUtils:
    def __init__(self, path: str) -> None:
        if not os.path.exists(path):
            raise FileNotExistException(f'File({path}) is not exists')
        self.path = path

    def clear(self):
        with open(self.path, "w") as f:
            f.write("")
