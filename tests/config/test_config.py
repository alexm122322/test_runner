from spytests._spytests.config import Config
from tests.consts import TEST_DIR


def test_ensure_session_created():
    config = Config(TEST_DIR)
    assert hasattr(config, 'session')


def test_ensure_test_config_created():
    config = Config(TEST_DIR)
    assert hasattr(config, 'test_config')


def test_ensure_session_logger_created():
    config = Config(TEST_DIR)
    assert hasattr(config, 'session_logger')


def test_ensure_test_results_logger_created():
    config = Config(TEST_DIR)
    assert hasattr(config, 'test_results_logger')
