from simple_test_runner._simple_test_runner.session import Session
from simple_test_runner._simple_test_runner.events.events import Events, SESSION_END, SESSION_START

from simple_test_runner import TestsConfig


def session_start1():
    pass


def session_start2():
    pass


def session_end1():
    pass


def session_end2():
    pass


def test_start_session_func_call(mocker):
    """Test session called session start function."""

    events = Events()
    mocked_session_start = mocker.patch(
        f'{__name__}.{session_start1.__name__}')

    session = Session(events, TestsConfig(), 'test/', [session_start1], [])
    session.start()
    mocked_session_start.assert_called_once()


def test_start_session_funcs_call(mocker):
    """Test session called session start functions."""

    events = Events()
    mocked_session_start1 = mocker.patch(
        f'{__name__}.{session_start1.__name__}')
    mocked_session_start2 = mocker.patch(
        f'{__name__}.{session_start2.__name__}')

    session = Session(events, TestsConfig(), 'test/',
                      [session_start1, session_start2], [])
    session.start()
    mocked_session_start1.assert_called_once()
    mocked_session_start2.assert_called_once()


def test_end_session_func_call(mocker):
    """Test session called session start function."""

    events = Events()
    mocked_session_end = mocker.patch(
        f'{__name__}.{session_end1.__name__}')

    session = Session(events, TestsConfig(), 'test/', [session_end1], [])
    session.start()
    mocked_session_end.assert_called_once()


def test_end_session_funcs_call(mocker):
    """Test session called session start functions."""

    events = Events()
    mocked_session_end1 = mocker.patch(
        f'{__name__}.{session_end1.__name__}')
    mocked_session_end2 = mocker.patch(
        f'{__name__}.{session_end2.__name__}')

    session = Session(events, TestsConfig(), 'test/',
                      [session_end1, session_end2], [])
    session.start()
    mocked_session_end1.assert_called_once()
    mocked_session_end2.assert_called_once()


def start_session_event():
    pass


def end_session_event():
    pass


def test_fire_start_event(mocker):
    """Test session fire start event."""

    events = Events()
    mocker = mocker.patch(f'{__name__}.{start_session_event.__name__}')

    def event_hendler(event):
        if event == SESSION_START:
            start_session_event()

    events.add_callback(event_hendler)
    session = Session(events, TestsConfig(), 'test/')
    session.start()
    mocker.assert_called_once()


def test_fire_end_event(mocker):
    """Test session fire end event."""

    events = Events()
    mocker = mocker.patch(f'{__name__}.{end_session_event.__name__}')

    def event_hendler(event):
        if event == SESSION_END:
            end_session_event()

    events.add_callback(event_hendler)
    session = Session(events, TestsConfig(), 'test/')
    session.start()
    mocker.assert_called_once()
    

def test_fire_collected_event(mocker):
    """Test session fire end event."""

    events = Events()
    mocker = mocker.patch('simple_test_runner._simple_test_runner.session.Session._collected')
    
    session = Session(events, TestsConfig(), 'test/')
    session.start()
    mocker.assert_called_once()
    
def test_fire_finished_event(mocker):
    """Test session fire end event."""

    events = Events()
    mocker = mocker.patch('simple_test_runner._simple_test_runner.session.Session._finished')
    
    session = Session(events, TestsConfig(), 'test/')
    session.start()
    mocker.assert_called_once()