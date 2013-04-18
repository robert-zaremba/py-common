from src.testutils import *
from functools import partial

def test_debug_print():
    f = debug_print("prefix")
    f("msg")

def test_fake_functionR():
    assert 2 == fake_functionR(2)
    assert 2 == fake_functionR(2, "das", [], {}, 123)

    assert 2 == partial(fake_functionR, 2, "das", [], {}, 123)("fda")

def test_numdict():
    nd = NumDict()
    assert nd[231] == 0
    assert nd['dfa'] == 0
    nd[5] += 1
    assert nd[5] == 1

def test_SpyCls():
    fake = SpyCls()
    fake.noexistancemethod()
    fake.noexistancemethod('31231', 312)
    assert fake.num_method_calls['noexistancemethod'] == 2


def test_partial_eq():
    partial_eq(55)(55)
    partial_eq('aa')('aa')

def test_partial_is():
    partial_is(55)(55)
