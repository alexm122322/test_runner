from typing import List
from logging import Logger

from ..test_cases import TestCases
from ..test_case_result import TestCaseResult
from ..test_case_results import TestCaseResults
from ..utils import TerminalUtils, DateTimeManager, get_system_info, item_count_str
from .formatters import ColorArgs


class BaseLogger:
    def __init__(self, logger: Logger):
        self.logger = logger


class SessionLogger(BaseLogger):
    def __init__(self, logger: Logger):
        super().__init__(logger)
        self.terminal_utils = TerminalUtils()
        self.date_time_manager = DateTimeManager()

    def log_session_start(self):
        self.logger.info(
            self.terminal_utils.create_full_str(' SESSION START ', '-'))
        self.logger.debug(get_system_info())
        self.logger.debug(self.date_time_manager.now)
        self.logger.debug('start at: {start_at}', ColorArgs(
            green={'start_at': self.date_time_manager.start_at()}))

    def log_session_end(self):
        self.logger.debug('finish at: {finish_at}', ColorArgs(
            green={'finish_at': self.date_time_manager.finish_at()}))
        self.logger.debug('total time: {total_time}', ColorArgs(
            green={'total_time': self.date_time_manager.running_time()}))
        self.logger.debug(
            self.terminal_utils.create_full_str(' SESSION END ', '-'))


class TestsLogger(BaseLogger):
    def __init__(self, logger: Logger):
        super().__init__(logger)
        self.terminal_utils = TerminalUtils()

    def log_test_cases_info(self, test_cases: TestCases):
        info = f"collect {item_count_str('items', test_cases.count)}: \n\n"
        for item in test_cases.items:
            info += f'{item.file_path} {len(item.test_cases)} cases \n'
        self.logger.debug(info)

    def log_results(self, test_results: TestCaseResults):
        for item in test_results.items:
            args = ColorArgs(green={'test_count': item.test_count,
                                    'passed_count': item.passed_count},
                             red={'failure_count': item.failure_count})
            self.logger.debug(item.module_test_case.file_path +
                              ' {test_count} test cases        {passed_count} passed, {failure_count} failed', args)

        self.logger.debug('\n')

        for item in test_results.items:
            if item.failure_results:
                self.logger.warn(self.terminal_utils.create_full_str(
                    f' {item.module_test_case.file_path} tests failures ', '='))
                self.log_failures(item.failure_results)
                self.logger.warn(self.terminal_utils.create_full_str(
                    f' {item.module_test_case.file_path} tests failures end ', '='))
                self.logger.debug('\n')

    def log_failures(self, results: List[TestCaseResult]):
        for failure in results:
            self.log_failure(failure)

    def log_failure(self, result: TestCaseResult):
        self.logger.error(f'"{result.test_case.method_name}" failure: \n')

        if result.exception:
            self.logger.error(f'{type(result.exception)} {result.exception}')
        if result.assertion_error:
            self.logger.error("Assertion Error")

        filename, line, func, text = result.stack_summary
        self.logger.error(f'{filename}, line {line} in {func}')
        self.logger.error(f'{text}')
        self.logger.debug('')

        if result.test_case.exception:
            self.logger.warn(f'expected {result.test_case.exception.__name__}')
            self.logger.debug('')
