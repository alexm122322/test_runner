# spytests
A python plugin for running and reporting tests. The plugin collects, runs, and reports about all simple tests in the directory. 

### Simple test example
```py
def test_equals():
    assert 1 == 1
```


## How to use
Run a command:

> spytests tests/

Where `tests/` is a `target directory`. The plugin collects all files which match with `test_files_pattern`. By default, it searches files that start with `test_`. And collects all methods which match with `test_funcs_pattern`. By default, it searches functions that start with `test_`.

## Setup

All setups are made in the `setup.py` file that is located inside the `target directory`.

### Start session

You are able to add callbacks that call when the session will be started like that:

```py
from spytests import start_session

@start_session
def session_start():
    pass
```

### End session

You are able to add callbacks that call when the session will be ended like that:

```py
from spytests import end_session

@end_session
def session_end():
    pass
```

### Test function should raise some Exception

You are able to mark some test the function that must raise an Exception like that:

```py
from spytests import raise_exception

class CustomError(Exception):
    pass

@raise_exception(CustomError)
def session_raise_custom_exception():
    raise CustomError('Exception for some reason.')
```

## TestsConfig

You are able to configure some extra parameters:

```py
from datatime import datatime
from spytests import TestsConfig, TextFormatter, FileFormatter, TestsLogger, SessionLogger

config = TestConfig(
    pythonpaths = ['.', 'src'],
    test_files_pattern = ['test_.*.py'],
    test_funcs_pattern = ['test_.*'],

    enable_print_to_file = False,
    print_file_name = 'test_report',
    print_file_format = '{name}_{datetime}.txt',
    print_file_datetime = datetime.now(),

    text_formatter = TextFormatter(),
    file_formatter = FileFormatter(),
    tests_logger = TestsLogger(),
    session_logger = SessionLogger(),
)
```

### pythonpaths

Path to your app/files. Adds to sys.path your path. By default `empty list`.

### test_files_pattern

Patterns for files detecting. By default `['test_.*.py']`.

### test_files_pattern

Patterns for functions detecting. By Default `['test_.*']`.

### enable_print_to_file

Enable printing report to file. By default `False`.

### print_file_name

Name of file. By default `'test_report'`.

### print_file_format

Format for print file name. By default `'{name}_{datetime}.txt',`. `{name}` and `{datetime}` are required.

### text_formatter

Text formatter customization. Should be a child of TextFormatter.

### file_formatter

File formatter customization. Should be a child of FileFormatter.

### tests_logger

Tests logger customization. Should be a child of TestsLogger.

### session_logger

Session logger customization. Should be a child of SessionLogger.
