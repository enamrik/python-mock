from typing import List, Any, Optional, Callable
from unittest.mock import Mock
from python_mock.setup import Setup
from python_mock.raise_exception import RaiseException
from python_mock.matcher import match_call_args
import re


class PyMock:
    mock_history = {}

    @staticmethod
    def new_mock(
            name: str,
            args=None,
            kwargs=None,
            return_values: Optional[List[Any]] = None,
            call_fake: Optional[Callable] = None):
        a_mock = Mock(name=name)
        PyMock.mock(a_mock, args, kwargs, return_values, call_fake)
        return a_mock

    @staticmethod
    def mock(a_mock,
             args=None,
             kwargs=None,
             return_values: Optional[List[Any]] = None,
             call_fake: Optional[Callable] = None,
             reset: bool = False):
        setup = Setup(args, kwargs, return_values, call_fake)
        if reset:
            PyMock.reset(a_mock)
        PyMock.__mock(a_mock, setups=[setup])
        return setup

    @staticmethod
    def reset(a_mock):
        if id(a_mock) not in PyMock.mock_history:
            raise Exception("This mock is not been configured by PyMock")
        del PyMock.mock_history[id(a_mock)]

    @staticmethod
    def calls(a_mock):
        if id(a_mock) not in PyMock.mock_history:
            raise Exception("This mock is not been configured by PyMock")
        return PyMock.mock_history[id(a_mock)]['calls']

    @staticmethod
    def get_setup(a_mock, index: int) -> Setup:
        mock_setups = PyMock.get_setups(a_mock)
        if 0 <= index <= len(mock_setups) - 1:
            return mock_setups[index]
        else:
            raise Exception("No setup at index {}. Setup count is {}".format(index, len(mock_setups)))

    @staticmethod
    def get_setups(a_mock) -> List[Setup]:
        if id(a_mock) not in PyMock.mock_history:
            raise Exception("This mock is not been configured by PyMock")
        return PyMock.mock_history[id(a_mock)]['setups']

    @staticmethod
    def __mock(a_mock, setups: List[Setup]):
        setup_return_history = {}

        if id(a_mock) not in PyMock.mock_history:
            PyMock.mock_history[id(a_mock)] = {'setups': [], 'calls': []}

        PyMock.mock_history[id(a_mock)]['setups'] = setups + PyMock.mock_history[id(a_mock)]['setups']

        def side_effect(*args, **kwargs):
            mock_setups = PyMock.mock_history[id(a_mock)]['setups']

            for cur_setup in mock_setups:
                setup: Setup = cur_setup
                setup_args = setup.args
                setup_kwargs = setup.kwargs
                call_fake = setup.call_fake

                did_match = match_call_args(args, kwargs, setup_args, setup_kwargs)

                if did_match:
                    if call_fake is not None:
                        return_value = call_fake({'args': args, 'kwargs': kwargs})
                        call_record = dict(method=PyMock.__mock_name(a_mock), args=list(args), kwargs=kwargs)
                        setup.append_call(call_record)
                        PyMock.mock_history[id(a_mock)]['calls'].append(call_record)
                    else:
                        if len(setup.return_values) == 0:
                            raise Exception("Setup return values cannot be empty: {}".format(setup))

                        return_index = setup_return_history[id(setup)] \
                            if id(setup) in setup_return_history \
                            else 0
                        if return_index < len(setup.return_values):
                            setup_return_history[id(setup)] = return_index + 1
                            return_value = setup.return_values[return_index]
                        else:
                            return_value = setup.return_values[-1]

                        call_record = dict(method=PyMock.__mock_name(a_mock), args=list(args), kwargs=kwargs)
                        setup.append_call(call_record)
                        PyMock.mock_history[id(a_mock)]['calls'].append(call_record)

                        if type(return_value) is RaiseException:
                            raise_exception: RaiseException = return_value
                            raise raise_exception.exception

                    return return_value

            error_message = \
                "NO MATCH FOUND for method {} with \n\n\targs:{}, \n\tkwargs:{}, \n\nMethod setups were:\n {}" \
                    .format(a_mock, list(args), kwargs, "\n".join(list(map(str, mock_setups))))
            print(error_message)
            raise CallNotFoundError("NO MATCH FOUND: See above for details")

        a_mock.side_effect = side_effect
        return a_mock

    @staticmethod
    def __mock_name(a_mock):
        return re.search(r'<.*Mock name=\'([a-zA-Z0-9._()-]+)\'', str(a_mock), re.IGNORECASE).group(1)


class CallNotFoundError(AssertionError):
    def __init__(self, message):
        self.message = message
