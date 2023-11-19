from typing import Any, Type, Callable, Never, Sequence, Mapping, Iterable
from functools import wraps
from dataclasses import dataclass

INF = float('inf')


@dataclass(slots=True)
class Scene:
    args_types: Sequence[Type]
    kwargs_types: Mapping[str, Type]


def gen_msg(o: tuple[Any, Any]):
    if o[0] is None:
        return ''
    return "{0}({2}) is not assignable to type {1}\n".format(repr(o[1]), *map(name_of, o[0]))


def name_of(obj: object):
    return getattr(obj, '__name__', repr(obj))


def _except_scenes(*scenes: Scene):
    def _inner(obj: Callable, *args, **kwargs):
        args_classes: Iterable[Type] = map(lambda a: type(a), args)
        kwargs_classes: dict[str, Type] = dict(map(lambda t: (t[0], type(t[1])), kwargs.items()))

        # scene_exc = []

        for scene in scenes:
            args_exceptions = []
            kwargs_exceptions = {}

            for key, args_class in enumerate(args_classes):
                excepted = None
                actual = None
                if not issubclass(args_class, scene.args_types[key]):
                    excepted = scene.args_types[key]
                    actual = args_class

                args_exceptions.append((excepted, actual) if excepted else None)

            for key, kwarg_class in kwargs_classes.items():
                excepted = None
                actual = None
                if not issubclass(kwarg_class, scene.kwargs_types[key]):
                    excepted = scene.kwargs_types[key]
                    actual = kwarg_class

                kwargs_exceptions[key] = (excepted, actual) if excepted else None

            if any(args_exceptions) or any(kwargs_exceptions.values()):
                raise TypeError(
                    f'excepted {obj.__name__}({", ".join(map(name_of, scene.args_types))}, '
                    f'{", ".join(map(lambda d: d[0] + "=" + name_of(d[1]), scene.kwargs_types.items()))}), '
                    f'got {obj.__name__}({", ".join(map(name_of, args))}, '
                    f'{", ".join(map(lambda d: d[0] + "=" + name_of(d[1]), kwargs.items()))})'

                    f'\n{"".join(map(gen_msg, zip(args_exceptions, args)))}'
                    f'\n{"".join(map(gen_msg, zip(kwargs_exceptions.values(), kwargs.values())))}'
                )

        return obj(*args, **kwargs)

    return _inner


def _except_range(maximum: int | Type[INF], minimum: int = 0) -> Callable[[Any, ...], None | Never]:
    def _inner(func: Callable, *args):
        if len(args) > maximum:
            raise TypeError(f'{func.__name__} excepted at most {maximum} argument, got {len(args)}')
        elif len(args) < minimum:
            raise TypeError(f'{func.__name__} excepted at least {minimum} argument, got 0')

    return _inner


def except_range(maximum: int | Type[INF], minimum: int = 0):
    validator = _except_range(maximum, minimum)

    def _deco(f: Callable):
        @wraps(f)
        def _wrapper(*args, **kwargs):
            validator(f, *args)
            return f(*args, **kwargs)

        return _wrapper

    return _deco
