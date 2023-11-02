from enum import IntEnum

from typing import final

@final
class ExitCode(IntEnum):
    """Encodes the valid exit codes by spytests."""

    #: spytests passed.
    OK = 0
    #: spytests failed.
    TESTS_FAILED = 1
    #: spytests was interrupted.
    INTERRUPTED = 2
    #: An internal error got in the way.
    INTERNAL_ERROR = 3
    #: spytests was misused.
    USAGE_ERROR = 4
    #: spytests couldn't find tests.
    NO_TESTS_COLLECTED = 5