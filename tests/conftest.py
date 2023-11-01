import os
import pytest
from mock import Mock
from tests.consts import TEST_DIR


@pytest.fixture
def find(mocker):
    return Mock()


@pytest.fixture(autouse=True, scope='session')
def prepare_test_dir(request):
    os.mkdir(TEST_DIR)
    yield
    os.rmdir(TEST_DIR)
