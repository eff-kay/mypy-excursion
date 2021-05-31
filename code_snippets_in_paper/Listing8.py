class ExtensionOpsMixin:
    # Fix to mitigate type errors
    # @classmethod
    # def _create_arithmetic_method(cls, op):  ...
    @classmethod
    def _add_arithmetic_ops(cls):
        cls.__add__ = cls._create_arithmetic_method(operator.add)

class BaseMaskedArray(ExtensionArray, ExtensionOpsMixin): 
    ...
    
class IntegerArray(BaseMaskedArray):
    @classmethod
    def _create_arithmetic_method(cls, op):  
        ...