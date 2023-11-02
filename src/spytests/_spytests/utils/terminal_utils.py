import os


class TerminalUtils:
    def __init__(self):
        try:
            self.terminal_width = os.get_terminal_size().columns
        except Exception:
            self.terminal_width = 100

    def create_full_str(self, title: str, sep: str):
        sep_count = int((self.terminal_width - len(title)) / 2)
        return f'{sep * sep_count}{title}{sep * sep_count}'
