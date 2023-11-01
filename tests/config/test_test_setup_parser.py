import os

from test_runner._test_runner.config.test_setup_parser import TestSetupParser, TEST_SETUP_FILE

from test_runner import TestsConfig

test_dir = 'test/'
start_session_name = 'custom_start_session'
end_session_name = 'custom_end_session'
config_name = 'test_config'
print_file_name = 'custom'


def _create_test_dir():
    """Creates a test dir, TEST_SETUP_FILE inside the test dir.
    Create test_* and check_* and fetch_*
    functions inside files.
    """

    os.mkdir(test_dir)

    with open(f'{test_dir}{TEST_SETUP_FILE}', "w") as f:
        f.write(f'''
from test_runner import TestsConfig, start_session, end_session

@start_session
def {start_session_name}():
    pass

@end_session
def {end_session_name}():
    pass
    
{config_name} = TestsConfig(print_file_name='{print_file_name}')
''')


def _remove_test_dir():
    """Removes TEST_SETUP_FILE, and test dir."""

    os.remove(f'{test_dir}{TEST_SETUP_FILE}')
    os.rmdir(test_dir)


def test_setup_parser_without_setup_file():
    """Test TestConfigParser without setup.py. 
    Should initialize session_end_callbacks 
    and session_start_callbacks with an empty lists. 
    test_config by default.
    """

    os.mkdir(test_dir)
    setup = TestSetupParser(test_dir).parse()

    test_config = setup[0]
    start_callbacks = setup[1]
    end_callbacks = setup[2]
    os.rmdir(test_dir)
    assert not start_callbacks
    assert not end_callbacks

    assert isinstance(test_config, TestsConfig)
    assert test_config.print_file_name != print_file_name


def test_setup_parser_should_parse():
    """Test TestConfigParser. Iside test_dir exists setup.py.
    In the setup.py presented start_session, and end_session functions.
    Custom TestsConfig attribute persists.
    """

    _create_test_dir()
    setup = TestSetupParser(test_dir).parse()
    _remove_test_dir()
    test_config = setup[0]
    start_callbacks = setup[1]
    end_callbacks = setup[2]

    assert len(start_callbacks) == 1
    assert len(end_callbacks) == 1

    assert start_callbacks[0].__name__ == start_session_name
    assert end_callbacks[0].__name__ == end_session_name

    assert isinstance(test_config, TestsConfig)
    assert test_config.print_file_name == print_file_name
