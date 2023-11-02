import logging

from typing import final


DEFAULT_LOG_FORMAT = "%(message)s"
DEFAULT_LOG_DATE_FORMAT = "%H:%M:%S"


class ColorCodes:
    grey = "\x1b[38;21m"
    green = "\x1b[1;32m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[1;34m"
    light_blue = "\x1b[1;36m"
    purple = "\x1b[1;35m"
    reset = "\x1b[0m"


@final
class ColorArgs:
    def __init__(self,  green: dict = None, red: dict = None):
        self.green = green
        self.red = red

    @property
    def count(self) -> int:
        count = 0
        if self.green:
            count += len(self.green)
        if self.red:
            count += len(self.red)
        return count

    @property
    def args_dict(self):
        result = {}
        if self.green:
            result.update(self._change_dict(self.green, ColorCodes.green))
        if self.red:
            result.update(self._change_dict(self.red, ColorCodes.red))
        return result

    def _change_dict(self, color_args: dict, color: str):
        result = {}
        for name, value in color_args.items():
            result[name] = (color, value)
        return result


class BaseFormatter(logging.Formatter):
    def format(self, record):
        self.rewrite_record(record, False)
        return super().format(record)
    
    def rewrite_record(self, record: logging.LogRecord, past_color: bool = False):
        msg = record.msg
        if not self._is_brace_format_style(record):
            return

        # add ANSI escape code for next alternating color before each formatting parameter
        # and reset color after it.
        if self._is_color_args(record.args):
            fixed = self._fix_color_args(msg, record.args[0], past_color)
            record.msg = fixed[0].format(*fixed[1])
            record.args = ()

    def _is_color_args(self, args) -> bool:
        return len(args) == 1 and isinstance(args[0], ColorArgs)

    def _fix_color_args(self, msg: str, args: ColorArgs, past_color: bool):
        args = args.args_dict
        msg = str(msg)
        fixed_args = []

        msg = msg.replace("{", "_{{")
        msg = msg.replace("}", "_}}")

        i: int = 0
        while True:
            if "_{{" not in msg:
                break

            start_index = msg.index("_{{")
            end_index = msg.index("_}}")
            name = msg[start_index + 3: end_index]
            if past_color:
                msg = msg.replace("_{{" + name, args[name][0] + "{", 1)
                msg = msg.replace("_}}", "}" + ColorCodes.reset, 1)
            else:
                msg = msg.replace("_{{" + name, "{", 1)
                msg = msg.replace("_}}", "}", 1)

            fixed_args.append(args[name][1])
            i += 1
        return (msg, tuple(fixed_args))

    def _is_brace_format_style(self, record: logging.LogRecord) -> bool:
        if len(record.args) == 0:
            return False

        msg = record.msg
        if '%' in msg:
            return False

        count_of_start_param = msg.count("{")
        count_of_end_param = msg.count("}")

        if count_of_start_param != count_of_end_param:
            return False

        if self._is_color_args(record.args) and record.args[0].count == count_of_start_param:
            return True

        return False


class TextFormatter(BaseFormatter):
    arg_colors = [ColorCodes.red, ColorCodes.light_blue]
    level_fields = ["levelname", "levelno"]
    level_to_color = {
        logging.DEBUG: ColorCodes.grey,
        logging.INFO: ColorCodes.green,
        logging.WARNING: ColorCodes.yellow,
        logging.ERROR: ColorCodes.red,
        logging.CRITICAL: ColorCodes.bold_red,
    }

    colors = {
        'green': ColorCodes.green,
        'red': ColorCodes.red,
    }

    def __init__(self):
        super().__init__()
        self.level_to_formatter = {}

        def add_color_format(level: int):
            color = TextFormatter.level_to_color[level]
            _format = color + DEFAULT_LOG_FORMAT + ColorCodes.reset
            formatter = logging.Formatter(_format)
            self.level_to_formatter[level] = formatter

        add_color_format(logging.DEBUG)
        add_color_format(logging.INFO)
        add_color_format(logging.WARNING)
        add_color_format(logging.ERROR)
        add_color_format(logging.CRITICAL)

    def format(self, record):
        orig_msg = record.msg
        orig_args = record.args
        formatter = self.level_to_formatter.get(record.levelno)
        self.rewrite_record(record, True)
        formatted = formatter.format(record)
        record.msg = orig_msg
        record.args = orig_args
        return formatted


class FileFormatter(BaseFormatter):
    pass
