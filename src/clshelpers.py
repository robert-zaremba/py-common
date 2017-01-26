from functools import wraps
import inspect


def lazy_init(fun):
    '''Automatically assigns function arguments (except keyword arguments)
to the object instance. This wrappers makes instance creation 3 times more
expensive in Python3.5 and 150x in PyPy3-5.5
Example:

    class X:
        @lazy_init
        def __init__(self, a1, a2, *args):

    x = X(1, 'two', 3, 4)

will assign only the listed arguments:

     x.a1 = 1
     x.a2 = 'two'
'''
    names, varargs, keywords, defaults = inspect.getargspec(fun)

    @wraps(fun)
    def wrapper(self, *args, **kwargs):
        for name, arg in zip(names[1:], args):
            setattr(self, name, arg)
        fun(self, *args, **kwargs)
    return wrapper
