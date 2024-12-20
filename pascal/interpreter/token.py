from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    OPERATOR = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOL = auto()
    ID = auto()
    ASSIGN = auto()
    SEMI = auto()
    BEGIN = auto()
    END = auto()
    DOT = auto()



class Token():
    def __init__(self, type_: TokenType, value: str):
        self.type_ = type_
        self.value = value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.type_}, {self.value})"