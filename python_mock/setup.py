from typing import List, Any, Optional, Callable


class Setup:
    def __init__(self,
                 args=None,
                 kwargs=None,
                 return_values: Optional[List[Any]] = None,
                 call_fake: Optional[Callable] = None):
        self.return_values = return_values if return_values is not None else []
        self.call_fake = call_fake
        if call_fake is not None and not callable(call_fake):
            raise Exception("Setup.call_fake must be function")
        self.args = args
        if args is not None and type(args) != list:
            raise Exception("Setup.args must be an array")
        self.kwargs = kwargs
        if kwargs is not None and type(kwargs) != dict:
            raise Exception("Setup.kwargs must be an dictionary")
        self.calls = []

    def append_call(self, call_args):
        self.calls.append(call_args)

    def __str__(self):
        return "\n\targs: {}, \n\tkwargs: {}, \n\treturn_values: {}".format(self.args, self.kwargs, self.return_values)

