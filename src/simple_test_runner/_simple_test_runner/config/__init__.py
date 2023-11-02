import os
import sys

from .exceptions import UsageError
from typing import Optional, Union
from .config import Config
from ..exit_code import ExitCode


def _directory_arg(path: str) -> str:
    """Argparse type validator for directory arguments.

    Args:
        path: Path of directory.
    """

    if not os.path.isdir(path):
        raise UsageError(f"must be a directory, given: {path}")
    return path


def _prepareconfig(
    args: Optional["os.PathLike[str]"] = None,
) -> Config:
    if args is None:
        dir_path = os.fspath(sys.argv[1:2][0])
        return Config(dir_path=_directory_arg(dir_path))
    else:
        dir_path = os.fspath(args)
        return Config(dir_path=_directory_arg(dir_path))


def main(
    args: Optional["os.PathLike[str]"] = None,
) -> Union[Config, ExitCode]:
    try:
        config = _prepareconfig(args)
        return config
    except Exception as e:
        return ExitCode.USAGE_ERROR
