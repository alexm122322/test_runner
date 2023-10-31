import enum
import os
import sys


from .exceptions import UsageError
from typing import List, Optional, Sequence, Union, final
from .config import Config

@final
class ExitCode(enum.IntEnum):
    """Encodes the valid exit codes by pytest.

    Currently users and plugins may supply other exit codes as well.

    .. versionadded:: 5.0
    """

    #: Tests passed.
    OK = 0
    #: Tests failed.
    TESTS_FAILED = 1
    #: pytest was interrupted.
    INTERRUPTED = 2
    #: An internal error got in the way.
    INTERNAL_ERROR = 3
    #: pytest was misused.
    USAGE_ERROR = 4
    #: pytest couldn't find tests.
    NO_TESTS_COLLECTED = 5

def directory_arg(path: str) -> str:
    """Argparse type validator for directory arguments.

    :path: Path of directory.
    :optname: Name of the option.
    """
    if not os.path.isdir(path):
        raise UsageError(f"must be a directory, given: {path}")
    return path


def _prepareconfig(
    args: Optional["os.PathLike[str]"] = None,
) -> Config:
    if args is None:
        dir_path = os.fspath(sys.argv[1:2][0])
        return Config(dir_path=directory_arg(dir_path))
    else:
        dir_path = os.fspath(args)
        return Config(dir_path=directory_arg(dir_path))
    
_PluggyPlugin = object

def main(
    args: Optional[Union[List[str], "os.PathLike[str]"]] = None,
    plugins: Optional[Sequence[Union[str, _PluggyPlugin]]] = None,
) -> Union[Config, ExitCode]:
    try:
        config = _prepareconfig(args)
        return config
    except Exception as e:
        print(f'error {e}')
        return ExitCode.USAGE_ERROR

