class Symbol:
    def __init__(self, name, type=None) -> None:
        self.name = name
        self.type = type


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name) -> None:
        super().__init__(name)

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name={self.name})>"


class VarSymbol(Symbol):
    def __init__(self, name, type) -> None:
        super().__init__(name, type)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(name={self.name}:type={self.type})>"
    
    __repr__ = __str__


class ScopedSymbolTable:
    def __init__(self, scope_name, scope_level, enclosing_scpe=None) -> None:
        self._symbols = {}
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scpe
        self._init_builtins()

        def _init_builtins(self):
            self.define(BuiltinTypeSymbol("INTEGER"))
            self.define(BuiltinTypeSymbol("REAL"))

        def __str__(self):
            return f"Symbols: {[value for value in self._symbols.values()]}"
        
        __repr__ = __str__

        def insert(self, symbol):
            print(f"Define: {symbol}" )
            self._symbols[symbol.name] = symbol

        def lookup(self, name):
            print(f"Lookup: {name}, (Scope name: {self.scope_name})")
            symbol = self._symbols.get(name)
            if symbol is not None:
                return symbol
            if self.enclosing_scope is not None:
                return self.enclosing_scope.lookup(name)
        

class ProcedureSymbol(Symbol):
    def __init__(self, name, params=None) -> None:
        super(ProcedureSymbol, self).__init__(name)
        self.params = params if params is not None else []

        def __str__(self):
            return f"<{self.__class__.__name__}(name={self.name}, parameters={self.params})>"
        
        __repr__ = __str__