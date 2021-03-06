import types
from Thrift.protocol.TProtocol import TProtocolBase

class TProtocolDecorator():
    def __init__(self, protocol):
        TProtocolBase(protocol)
        self.protocol = protocol

    def __getattr__(self, name):
        if hasattr(self.protocol, name):
            member = getattr(self.protocol, name)
            if type(member) in [
                types.MethodType,
                types.FunctionType,
                types.LambdaType,
                types.BuiltinFunctionType,
                types.BuiltinMethodType,
            ]:
                return lambda *args, **kwargs: self._wrap(member, args, kwargs)
            else:
                return member
        raise AttributeError(name)

    def _wrap(self, func, args, kwargs):
        if isinstance(func, types.MethodType):
            result = func(*args, **kwargs)
        else:
            result = func(self.protocol, *args, **kwargs)
        return result
