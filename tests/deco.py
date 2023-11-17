from typing import Callable
from unittest import TestCase
from utils.decos import _except_scenes, Scene, name_of, gen_msg


class TestExceptScene(TestCase):
    def test_basic_type(self):
        def func():
            pass

        with self.assertRaises(TypeError) as cm:
            _except_scenes(Scene([int, str], {'a': str}))(func, 114, 514, a=191)

        self.assertEqual(
            str(cm.exception),
            f'excepted {name_of(func)}(int, str, a=str), got {name_of(func)}(114, 514, a=191)\n'
            + gen_msg(((str, int), 514)) + '\n'
            + gen_msg(((str, int), 191))
        )

        _except_scenes(Scene([bytes, int], {'key': int}))(lambda: None, b'Hello World', 1145, key=141)

    def test_generic_type(self):
        _except_scenes(Scene([Callable, str], {'a': int}))(lambda a: None, lambda: None, '114', a=514)
