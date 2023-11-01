from enum import IntEnum

from typing import final

@final
class ExitCode(IntEnum):
    """Encodes the valid exit codes by test_runner."""

    #: test_runner passed.
    OK = 0
    #: test_runner failed.
    TESTS_FAILED = 1
    #: test_runner was interrupted.
    INTERRUPTED = 2
    #: An internal error got in the way.
    INTERNAL_ERROR = 3
    #: test_runner was misused.
    USAGE_ERROR = 4
    #: test_runner couldn't find tests.
    NO_TESTS_COLLECTED = 5