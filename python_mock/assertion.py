from typing import Optional
from python_mock.print_call import print_call
from python_mock.py_mock import PyMock
from difflib import ndiff
from python_mock.compare_dict import is_same_dict
from python_mock.matcher import match_call_args


def assert_same_dict(dict1, dict2):
    same, result = is_same_dict(dict1, dict2)
    assert same, "Should be the same. Instead got diff: {}".format(result)


def assert_that(mock):
    return Assertion(mock)


class Assertion:
    def __init__(self, mock):
        self.mock = mock

    def call_count(self, count):
        setups = PyMock.get_setups(self.mock)
        mock_call_count = 0
        for setup in setups:
            mock_call_count += len(setup.calls)

        if not count == mock_call_count:
            raise MatchAssertionError("Expect call count {}. Got {}".format(count, mock_call_count))

    def was_not_called(self, with_args=None, with_kwargs=None, times=None, exactly_times=None):
        self.was_called(with_args, with_kwargs, times, exactly_times, negate=True)

    def was_called(self, with_args=None, with_kwargs=None,
                   times=None, exactly_times=None, negate: bool = False):

        match_count = 0
        setups = PyMock.get_setups(self.mock)
        for setup in setups:
            for call in setup.calls:
                call_args = call['args']
                call_kwargs = call['kwargs']
                setup_args = with_args
                setup_kwargs = with_kwargs

                match = match_call_args(call_args, call_kwargs, setup_args, setup_kwargs)
                if match:
                    match_count += 1

        Assertion.__assert_call_count(
            {'args': with_args, 'kwargs': with_kwargs},
            self.__all_calls(),
            match_count, times, exactly_times, negate)

    def __all_calls(self):
        all_calls = []
        setups = PyMock.get_setups(self.mock)
        for setup in setups:
            all_calls += setup.calls
        return all_calls

    @staticmethod
    def __assert_call_count(call, calls,
                            match_count: int,
                            times: Optional[int] = None,
                            exactly_times: Optional[int] = None,
                            negate: bool = False):

        times = 1 if times is None else times

        times_text = 'exactly ' + str(exactly_times) \
            if exactly_times is not None \
            else str(times) + ' or more'

        negate_text = ' not ' if negate else ' '

        bool_exp = match_count == exactly_times \
            if exactly_times is not None \
            else match_count >= times

        if negate:
            bool_exp = not bool_exp

        expected_call_text = print_call(call['args'], call['kwargs'])

        diffs = list(map(
            lambda x: ''.join(
                ndiff(
                    expected_call_text.splitlines(True),
                    print_call(x['args'], x['kwargs']).splitlines(True)
                )),
            calls))

        if not bool_exp:
            raise MatchAssertionError(
                "Expected to{}have been called {} times. But call count was: {}. "
                "\n\nExpected call:\n{}"
                "\n\nActual calls compared to expected call:\n{}"
                    .format(negate_text,
                            times_text,
                            match_count,
                            expected_call_text,
                            '\n'.join(diffs))
            )


class MatchAssertionError(AssertionError):
    def __init__(self, message):
        self.message = message
