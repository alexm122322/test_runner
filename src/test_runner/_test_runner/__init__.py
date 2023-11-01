import os
from typing import List, Optional, Union
from .config import main as config_main
from .exit_code import ExitCode


def main(
    args: Optional[Union[List[str], "os.PathLike[str]"]] = None,
) -> ExitCode:
    """Main function for test_runner.

    Args:
        args: Arguments. Defaults to None. For test only.

    Returns:
        ExitCode: test_runner exit code.
    """

    try:
        config = config_main(args)
        if isinstance(config, ExitCode):
            return config

        return config.session.start()
    except KeyboardInterrupt:
        return ExitCode.INTERRUPTED
    except Exception:
        return ExitCode.INTERNAL_ERROR
