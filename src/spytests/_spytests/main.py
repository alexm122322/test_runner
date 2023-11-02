from types import FunctionType
from .test_case_collector import TestCaseCollector
from .test_case_runner import TestCaseRunner
from .exit_code import ExitCode
from .config.test_config import TestsConfig


def run_tests(
    config: TestsConfig,
    dir_path: str,
    collected: FunctionType,
    finished: FunctionType,
) -> ExitCode:
    """Collect and running tests.

    Args:
        config: spytests configuration.

    Returns:
        ExitCode: spytests exit code.
    """
    collector = TestCaseCollector(config, dir_path)
    runner = TestCaseRunner()

    test_cases = collector.collect()
    collected(test_cases)
    results = runner.run_test_cases(test_cases)
    finished(results)

    return ExitCode.OK if results.all_passed else ExitCode.TESTS_FAILED
