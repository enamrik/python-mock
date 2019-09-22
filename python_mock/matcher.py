from python_mock.compare_dict import is_same_dict
from typing import Callable, Any


class MatchArg:
    @staticmethod
    def any():
        return {'__match__': '<Any>'}

    @staticmethod
    def match(func: Callable[[Any], bool]):
        return {'__match__': func}


def match_call_args(call_args, call_kwargs, setup_args, setup_kwargs):
    match = True

    if setup_args is not None and len(setup_args) > 0:
        if len(setup_args) != len(call_args):
            match = False
        if match:
            for idx, arg in enumerate(call_args):
                if not args_match(arg, setup_args[idx]):
                    match = False
                    break
    if setup_kwargs is not None and len(setup_kwargs.keys()) > 0:
        if len(setup_kwargs.keys()) != len(call_kwargs.keys()):
            match = False
        if match:
            for key, value in setup_kwargs.items():
                if not (key in setup_kwargs and args_match(value, setup_kwargs[key])):
                    match = False
                    break
    return match


def args_match(arg, setup_arg):
    if type(setup_arg) == dict and '__match__' in setup_arg:
        match_info = setup_arg['__match__']
        if type(match_info) == str and match_info == '<Any>':
            return True
        if type(match_info) == dict:
            same, _ = is_same_dict(arg, match_info)
            return same
        if callable(match_info):
            func: Callable[[Any], bool] = match_info
            return func(arg)
    else:
        return arg == setup_arg


