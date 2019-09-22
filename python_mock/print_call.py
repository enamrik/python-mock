from typing import Any, List


def print_call(args: List[Any], kwargs: dict):
    if kwargs is None:
        kwargs = {}
    if args is None:
        args = []

    def _print_val(arg):
        if type(arg) == dict and '__match__' in arg:
            match_info = arg['__match__']
            if type(match_info) == str and match_info == '<Any>':
                return "<Any>"
            if type(match_info) == dict:
                return "{}".format(match_info)
            if callable(match_info):
                return "{}".format(match_info)
        if type(arg) == list:
            print_arg = lambda x: '\t{}: {}'.format(x[0], _print_val(x[1]))
            return '\n'.join(list(map(print_arg, enumerate(list(args)))))
        if type(arg) == str:
            return arg.replace('\n', '\n\t   ')
        if type(arg) == dict:
            return '\n\t   '.join(list(map(lambda x: '{}: {}'.format(x[0], _print_val(x[1])), arg.items())))
        if type(arg) == tuple:
            return _print_val(list(arg))
        return '\n\t   {}'.format(arg)

    return '\nargs:{}\nkwargs:{}'.format(_print_val(args), _print_val(kwargs))
