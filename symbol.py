class Symbol:
    def __init__(self, name, type=None) -> None:
        self.name = name
        self.type = type


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name) -> None:
        super().__init__(name)

    def __str__(self) -> str:
        return self.name
    
    __repr__ = __str__


class VarSymbol(Symbol):
    def __init__(self, name, type) -> None:
        super().__init__(name, type)

    def __str__(self) -> str:
        return f"<{self.name}:{self.type}>"
    
    __repr__ = __str__


class SymbolTable:
    def __init__(self) -> None:
        self._symbols = {}
        self._init_builtins()

        def _init_builtins(self):
            self.define(BuiltinTypeSymbol("INTEGER"))
            self.define(BuiltinTypeSymbol("REAL"))

        def __str__(self):
            return f"Symbols: {[value for value in self._symbols.values()]}"
        
        __repr__ = __str__

        def define(self, symbol):
            print("Define: %s" % symbol)
            self._symbols[symbol] = symbol

        def lookup(self, name):
            print("Lookup: %s" % name)
            return self._symbols.get(name)
        
