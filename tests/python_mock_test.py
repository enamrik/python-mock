from python_mock import PyMock, assert_that, MatchArg
from unittest.mock import Mock

from python_mock.assertion import MatchAssertionError
from python_mock.py_mock import CallNotFoundError


def test_can_mock_method():
    prop1 = Mock(name="test_class.prop1")
    PyMock.mock(prop1, return_values=[1])
    assert prop1() == 1


def test_can_setup_and_create_mock_in_one_step():
    prop1 = PyMock.new_mock(name="test_class.prop1", return_values=[1])
    assert prop1() == 1


def test_can_assert_mock_call_count():
    prop1 = PyMock.new_mock(name="test_class.prop1", return_values=[1])
    prop1()
    prop1()
    assert_that(prop1).call_count(2)

    assert_exception(
        lambda: assert_that(prop1).call_count(1),
        "Expect call count 1. Got 2")


def test_can_assert_different_setups():
    mock = Mock(name="test_class.prop1")
    PyMock.mock(mock, args=[1, 1], return_values=[1])
    PyMock.mock(mock, args=[2, 2], return_values=[2])
    mock(1, 1)
    mock(1, 1)
    mock(2, 2)

    assert_that(mock).was_called(with_args=[1, 1], exactly_times=2)

    assert_exception(
        lambda: assert_that(mock).was_called(with_args=[1, 1], exactly_times=1),
        "Expected to have been called exactly 1 times. But call count was: 2")

    assert_that(mock).was_called(with_args=[2, 2], exactly_times=1)

    assert_exception(
        lambda: assert_that(mock).was_called(with_args=[2, 2], exactly_times=2),
        "Expected to have been called exactly 2 times. But call count was: 1")


def test_can_make_negative_assertion():
    mock = Mock(name="test_class.prop1")
    PyMock.mock(mock, args=[1], return_values=[1])

    assert_that(mock).was_not_called(with_args=[1])

    mock(1)
    assert_exception(
        lambda: assert_that(mock).was_not_called(with_args=[1]),
        "Expected to not have been called 1 or more times. But call count was: 1")


def test_can_match_any_arg():
    mock = Mock(name="test_class.prop1")
    PyMock.mock(mock, return_values=[1])
    mock(1, 4)
    assert_that(mock).was_called(with_args=[1, MatchArg.any()])

    assert_exception(
        lambda: assert_that(mock).was_called(with_args=[2, MatchArg.any()]),
        "Expected to have been called 1 or more times. But call count was: 0")


def test_can_mock_any_arg():
    mock = Mock(name="test_class.prop1")
    PyMock.mock(mock, args=[1, MatchArg.any()], return_values=[1])
    result = mock(1, 4)
    assert result == 1


def test_can_match_dict_arg():
    mock = Mock(name="test_class.prop1")
    PyMock.mock(mock, return_values=[1])
    mock({'a': 1, 'b': {'d': 6}})
    assert_that(mock).was_called(with_args=[{'a': 1, 'b': {'d': 6}}])

    assert_exception(
        lambda: assert_that(mock).was_called(with_args=[{'c': 3, 'd': 4}]),
        "Expected to have been called 1 or more times. But call count was: 0")


def test_can_match_custom_matcher():
    mock = Mock(name="test_class.prop1")
    PyMock.mock(mock, return_values=[1])
    mock(4)
    assert_that(mock).was_called(with_args=[MatchArg.match(lambda x: x == 4)])

    assert_exception(
        lambda: assert_that(mock).was_called(with_args=[MatchArg.match(lambda x: x == 5)]),
        "Expected to have been called 1 or more times. But call count was: 0")


def test_can_get_mock_calls():
    mock = Mock(name="test_class.prop1")
    PyMock.mock(mock, return_values=[1])
    mock(4)
    mock(5)
    calls = PyMock.calls(mock)
    assert calls[0]['args'][0] == 4
    assert calls[1]['args'][0] == 5


def assert_exception(action, message):
    def _run_action():
        try:
            action()
            raise Exception("No exception was raised for action")
        except CallNotFoundError as e:
            return e
        except MatchAssertionError as e:
            return e
    result = _run_action()
    assert message in result.message, "Message {} does not contain {}".format(result.message, message)

