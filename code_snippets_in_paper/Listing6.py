class _MovedItems(_LazyModule):
    __path__ = []
    # annotation fix for 5.4.2
    #__path__:List[str] = []
    # annotation fix for 5.4.3
    #builtins:List[str]

_moved_attributes = [...]
for attr in _moved_attributes:
    setattr(_MovedItems, attr.name, attr)

_MovedItems._moved_attributes = _moved_attributes

moves = _MovedItems(__name__ + ".moves")
exec_ = getattr(moves.builtins, "exec")