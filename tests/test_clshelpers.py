from src.clshelpers import lazy_init


class X:
    @lazy_init
    def __init__(self, a1, a2, *args, **kwargs):
        pass

    def m(self):
        pass


def test_lazy_init():
    x = X('p1', 'p2', 'extra', check=True)

    assert vars(x) == {'a1': 'p1', 'a2': 'p2'}
