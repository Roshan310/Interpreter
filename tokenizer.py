class Token:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f"Token({self.type}, {self.value})"

    def __repr__(self) -> str:
        return self.__str__()
