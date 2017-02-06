from pycommon.clshelpers import lazy_init
# from pycommon.clshelpers import lazy_init


class X:
    def __init__(self, a, b, c, d, *args):
        self.a = a
        self.b = b
        self.c = c
        self.d = d


class XLazy:
    @lazy_init
    def __init__(self, a, b, c, d, *args):
        pass


if __name__ == '__main__':
    from timeit import timeit

    print("X:")
    print(timeit("X(1,2,3,4)", "from __main__ import X"))

    print("XLazy:")
    print(timeit("XLazy(1,2,3,4)", "from __main__ import XLazy"))
