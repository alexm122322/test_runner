import logging

from typing import Dict, Tuple, final

DEFAULT_LOG_FORMAT = "%(message)s"


class ColorCodes:
    """Color codes for terminal. """
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
    """Argument class which contain args filtered by colors.
    Supporting collors: green, red.
    """

    def __init__(self, green: dict = None, red: dict = None):
        self.green = green
        self.red = red

    @property
    def count(self) -> int:
        """Counts all colors arguments.

        Returns:
            int: Count.
        """
        count = 0
        if self.green:
            count += len(self.green)
        if self.red:
            count += len(self.red)
        return count

    @property
    def args_dict(self) -> Dict:
        """Convert args to dict. 

        Returns:
            Dict: Dict of ColorArgs. Format: [name] = tuple(color_code, value)
        """
        result = {}
        if self.green:
            result.update(self._change_dict(self.green, ColorCodes.green))
        if self.red:
            result.update(self._change_dict(self.red, ColorCodes.red))
        return result

    def _change_dict(self, color_args: dict, color: str):
        """Util funct wich help convert args to dict.

        Returns:
            Dict: Dict of ColorArgs. Format: [name] = tuple(color_code, value)
        """
        result = {}
        for name, value in color_args.items():
            result[name] = (color, value)
        return result


class BaseFormatter(logging.Formatter):
    """Base implementation of logging Formatter. """

    def format(self, record):
        self.rewrite_record(record, False)
        return super().format(record)

    def rewrite_record(self, record: logging.LogRecord, put_color: bool = False):
        """Rewriting records. Detects ColorArgs and reformats a record.
        Changing Record.

        Args:
            record: Log Record.
            put_color: Need to put collor to record. True if needed.
        """
        msg = record.msg
        if not self._is_brace_format_style(record):
            return

        if self._is_color_args(record.args):
            fixed = self._fix_color_args(msg, record.args[0], put_color)
            record.msg = fixed[0].format(*fixed[1])
            record.args = ()

    def _is_color_args(self, args) -> bool:
        """Detect if arguments contain ColorArgs.

        Args:
            args: Arguments of record.
        Return: 
            bool: True if args contains ColorArgs.
        """

        return len(args) == 1 and isinstance(args[0], ColorArgs)

    def _fix_color_args(self, msg: str, args: ColorArgs, put_color: bool) -> Tuple:
        """Fixes message and arguments.

        Args:
            msg: Message in Record.
            args: Color arguments.
            put_color: Need or not put colors wrappers. True if needed. 

        Returns:
            Tuple (Message, (List)): Fixed meaasge and arguments.
        """
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
            if put_color:
                msg = msg.replace("_{{" + name, args[name][0] + "{", 1)
                msg = msg.replace("_}}", "}" + ColorCodes.reset, 1)
            else:
                msg = msg.replace("_{{" + name, "{", 1)
                msg = msg.replace("_}}", "}", 1)

            fixed_args.append(args[name][1])
            i += 1
        return (msg, tuple(fixed_args))

    def _is_brace_format_style(self, record: logging.LogRecord) -> bool:
        """Check if contains brace arguments. Example: `{arg}`.

        Args:
            record: Log record.

        Return:
            bool: True if contained. False otherwise.
        """
        if not record.args:
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
    """Implementation of color text Formatter.

    Args:
        level_to_formatter: Mapping level to formatter.
    """

    level_to_color = {
        logging.DEBUG: ColorCodes.grey,
        logging.INFO: ColorCodes.green,
        logging.WARNING: ColorCodes.yellow,
        logging.ERROR: ColorCodes.red,
        logging.CRITICAL: ColorCodes.bold_red,
    }

    def __init__(self):
        super().__init__()
        self.level_to_formatter: Dict[int, str] = {}

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

    def format(self, record) -> str:
        """Format message. Changes message using rewrite_record method.

        Args:
            record: Formatting record.

        Returns:
            str: Formatted message.
        """
        formatter = self.level_to_formatter.get(record.levelno)
        self.rewrite_record(record, True)
        formatted = formatter.format(record)

        return formatted


class FileFormatter(BaseFormatter):
    """Default implementation of BaseFormatter for File"""
    pass
