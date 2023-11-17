try:
    from rich.pretty import pprint
except ImportError:
    pass


class TypeMisMatchError(TypeError):
    def __init__(self, args, kwargs)
