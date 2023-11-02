from spytests._spytests.events import Events

EVENT1 = 'event1'
EVENT2 = 'event2'


def event_handler(event: str):
    """Simple event handler for test.

    Args:
        event: events.
    """
    if event == EVENT1:
        event1()
    elif event == EVENT2:
        event2()


def event1():
    pass


def event2():
    pass


def test_add_event_handler(mocker):
    """Test Events.add_callback. Events should be triggered."""
    events = Events()
    mock = mocker.patch(f'{__name__}.{event1.__name__}')
    events.add_callback(event_handler)
    events.fire_event(EVENT1)
    mock.assert_called_once()


def test_remove_event_handler(mocker):
    """Test Events.remove_callback. 
    Events shouldn't be triggered after event_handler is removed."""
    events = Events()
    event1_mock = mocker.patch(f'{__name__}.{event1.__name__}')
    event2_mock = mocker.patch(f'{__name__}.{event2.__name__}')
    events.add_callback(event_handler)

    events.fire_event(EVENT1)
    event1_mock.assert_called_once()

    events.remove_callback(event_handler)

    events.fire_event(EVENT2)
    event2_mock.assert_not_called()


def test_triger_events(mocker):
    """Test Events.fire_event. Events should be triggered."""
    events = Events()
    event1_mock = mocker.patch(f'{__name__}.{event1.__name__}')
    event2_mock = mocker.patch(f'{__name__}.{event2.__name__}')
    events.add_callback(event_handler)

    events.fire_event(EVENT1)
    event1_mock.assert_called_once()

    events.fire_event(EVENT2)
    event2_mock.assert_called_once()
