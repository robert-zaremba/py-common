from multiprocessing import Event

print("W test utils")

def debug_print(prefix):
    def partial(data, callback=None):
        print(str(prefix) + str(data)+'#')
        if callback: callback(data)
    return partial

def partial_eq(x):
    """function for partial callbacks to test equality assertion.

    In the following expression, function f is called asynchronously and the
    result is passed to callback:

        do_async(f, callback=partial_eq(10))

    equals to synchronized expression:

        partial_eq(10)( f() )
    """
    def partial(y):
        assert x == y
    return partial

def partial_is(x):
    """analogously to parital_eq
    read help from function partial_eq for more information
    """
    def partial(y):
        assert x is y
    return partial



class NumDict(dict):
    def __getitem__(self, key):
        return self.get(key, 0)


def fake_function(*args, **kwargs):
    """fake function which acceept any argument and returns None"""
    pass

def fake_functionR(to_return, *args, **kwargs):
    """Function which takes at least 1 argument and return it.
    Can be used with functools.partial"""
    return to_return


class FakeCls(object):
    """Fake class  which accepts every field, and returns <ret_val>, which
    is `fake function` as default"""
    def __init__(self, ret_val=fake_function):
        self.ret_val = ret_val

    def __getattr__(self, name):
        """this is runned if self.name fails"""
        return self.ret_val


class SpyCls(object):
    """type for test which trace object usage:
      it allows to access any field / method
      it counts number of getting / calling   fields / methods
      """

    def __init__(self, ret_val=fake_function):
        self.num_method_calls = NumDict()
        self.ret_val = ret_val

    def __getattr__(self, name):
        """this is runned if self.name fails"""
        self.num_method_calls[name] += 1
        return self.ret_val

class SpyMethod(SpyCls):
    """like SpyCls but also, object of this class acts as method, which acceppt any arguments and
    returns None.
    It counts calls of the method, so after test we can check if
    the method (object) was called and how many times"""
    def __init__(self):
        self.num_calls = 0
    def __call__(self, *args, **kwargs):
        self.num_calls += 1

class SpyCallbackMethod(SpyMethod):
    """Like SpyMethod, but expects callable as a first argument
    and call it with rest of arguments"""
    def __call__(self, f, *args, **kwargs):
        super(SpyCallbackMethod, self).__call__(f, *args, **kwargs)
        return f(*args, **kwargs)


def wrap_with_event_beginning(obj, fun_name):
    """wrap obj.fun_name function with event set at the beginning of the
    function"""
    e = Event()
    orig = obj.__getattribute__(fun_name)
    def wrapper():
        e.set()
        orig()
    obj.__setattr__(fun_name, wrapper)
    return e

def wrap_with_event_ending(obj, fun_name):
    """wrap obj.fun_name function with event set at the ending of the
    function"""
    e = Event()
    orig = obj.__getattribute__(fun_name)
    def wrapper():
        orig()
        e.set()
    obj.__setattr__(fun_name, wrapper)
    return e
