from typing import List
from logging import Logger

from ..test_cases import TestCases
from ..test_case_result import TestCaseResult, ModuleTestCaseResult
from ..test_case_results import TestCaseResults
from ..utils import TerminalUtils, DateTimeManager, get_system_info, item_count_str
from .formatters import ColorArgs


class BaseLogger:
    def __init__(self, logger: Logger):
        self.logger = logger

    def _br(self):
        """Print '\n'"""
        self.logger.debug('')


class SessionLogger(BaseLogger):
    """Session logging.

    Args:
        logger: Logger for Session logging.
        terminal_utils: Utils for terminal.
        date_time_manager: Manager of data time.
    """

    def __init__(self, logger: Logger):
        super().__init__(logger)
        self.terminal_utils = TerminalUtils()
        self.date_time_manager = DateTimeManager()

    def log_session_start(self):
        """Prints about the session start.
        Print Information about system, start time.
        """
        self.logger.info(
            self.terminal_utils.create_full_str(' SESSION START ', '-'))
        self.logger.debug(get_system_info())
        self.logger.debug(self.date_time_manager.now)
        self.logger.debug('start at: {start_at}', ColorArgs(
            green={'start_at': self.date_time_manager.start_at()}))

    def log_session_end(self):
        """Prints about the session end.
        Print information about end time and running total time.
        """
        self.logger.debug('finish at: {finish_at}', ColorArgs(
            green={'finish_at': self.date_time_manager.finish_at()}))
        self.logger.debug('total time: {total_time}', ColorArgs(
            green={'total_time': self.date_time_manager.running_time()}))
        self.logger.debug(
            self.terminal_utils.create_full_str(' SESSION END ', '-'))


class TestsLogger(BaseLogger):
    """Tests logging.

    Args:
        logger: Logger for Session logging.
        terminal_utils: Utils for terminal.
    """

    def __init__(self, logger: Logger):
        super().__init__(logger)
        self.terminal_utils = TerminalUtils()

    def log_test_cases_info(self, test_cases: TestCases):
        """Prints info about collected test cases.

        Args:
            test_cases: Collected test cases.
        """
        info = f"collect {item_count_str('items', test_cases.count)}: \n\n"
        for item in test_cases.items:
            info += f'{item.file_path} {len(item.test_cases)} cases \n'
        self.logger.debug(info)

    def log_results(self, test_results: TestCaseResults):
        """Prints info about test results.

        Args:
            test_results: Test Results.
        """
        for item in test_results.items:
            args = ColorArgs(green={'test_count': item.test_count,
                                    'passed_count': item.passed_count},
                             red={'failure_count': item.failure_count})

            self.logger.debug(self._module_result_str(item), args)

        self.logger.debug('\n')

        for item in test_results.items:
            file_path = item.module_test_case.file_path
            if item.failure_results:
                self.logger.warning(self.terminal_utils.create_full_str(
                    f' {file_path} tests failures ', '='))
                self._log_failures(item.failure_results)
                self.logger.warning(self.terminal_utils.create_full_str(
                    f' {file_path} tests failures end ', '='))
                self.logger.debug('\n')

    def _log_failures(self, results: List[TestCaseResult]):
        """Prints info about failures.

        Args:
            results: Test results.
        """
        for failure in results:
            self._log_failure(failure)

    def _log_failure(self, result: TestCaseResult):
        """Prints info about failure.

        Args:
            result: Test result.
        """
        self.logger.error(f'"{result.test_case.method_name}" failure: \n')

        if result.exception is not None:
            self.logger.error(f'{type(result.exception)} {result.exception}')

        if result.assertion_error is not None:
            self.logger.error("Assertion Error")

        if (result.test_case.exception is not None and
                result.stack_summary is not None):
            filename, line, func, text = result.stack_summary
            self.logger.error(f'{filename}, line {line} in {func}')
            self.logger.error(f'{text}')
            self._br()

        if result.test_case.exception is not None:
            self.logger.warning(f'expected {result.test_case.exception.__name__}')
            self._br()

    def _module_result_str(self, result: ModuleTestCaseResult) -> str:
        """Creates str for module result logging.

        Args:
            result: Result of module testing.

        Returns:
            str: Module result logging string.
        """
        start = result.module_test_case.file_path
        test_cases_count = item_count_str('case', result.test_count)
        middle = ' {test_count} test ' + test_cases_count
        end = '        {passed_count} passed, {failure_count} failed'

        return f'{start} {middle} {end}'
