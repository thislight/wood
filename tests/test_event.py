

from unittest.mock import Mock
from wood.support import event

def clean():
    event.EventManager.clean_env()

def test_can_add_callback():
    clean()
    callback_function = Mock()

    event.EventManager.callback('test',callback_function)

    assert callback_function in event.EventManager.callbacks['test']


def test_can_call_callback():
    clean()
    event.EventManager.call('test')

    assert len(event.EventManager.event_queue) > 0


def test_can_clean_queue():
    clean()
    event.EventManager.call('test')

    event.EventManager.finish_queue()

    assert len(event.EventManager.event_queue) == 0


def test_manager_can_call_event_callback():
    clean()
    callback_function = Mock()
    callback_function._mock_unsafe = True
    event.EventManager.callback('test',callback_function)
    callback_function.assert_not_called()

    event.EventManager.call('test')
    event.EventManager.finish_queue()

    callback_function.assert_called_once()

