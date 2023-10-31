import os
from typing import List, Optional, Union
from .config import main as config_main
from .config import ExitCode
from .test_case_collector import TestCaseCollector
from .test_case_runner import TestCaseRunner
from .events.events import SESSION_START, SESSION_END

    
def main(
    args: Optional[Union[List[str], "os.PathLike[str]"]] = None,
):
    config = config_main(args)
    if isinstance(config, ExitCode):
        return ExitCode
    session = config.get_session
    session.start()
    collector = TestCaseCollector(config.test_config)
    runner = TestCaseRunner()
    test_cases = collector.collect(config.dir_path)
    config.test_results_logger.log_test_cases_info(test_cases)
    results = runner.run_test_cases(test_cases)
    config.test_results_logger.log_test_case_results(results)
    session.end()
    