from src.test_runner import start_session, end_session, TestsConfig


@start_session
def start():
    print('session start')


@end_session
def end():
    print('session end')


test_config = TestsConfig(
    enable_print_to_file=True,
    print_file_path= 'tests/print.txt'
)