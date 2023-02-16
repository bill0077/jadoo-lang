"""module for jadoo lang"""
from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    """token type of jadoo lang"""

    # mark
    PAREN_OPEN = auto()
    PAREN_CLOSE = auto()
    EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLE = auto()
    DIVISION = auto()
    SINGLE_QUOTES = auto()
    DOUBLE_QUOTES = auto()
    BLANK = auto()
    BREAKLINE = auto()

    # data type
    INTEGER = auto()
    STRING = auto()

    # keyword
    PRINT = auto()
    WHILE = auto()
    IF = auto()
    JADOO = auto()
    DOO = auto()

    # other
    NONE = auto()
    TEMP = auto()
    VARNAME = auto()

mark_literal : list[str] = ["" for i in range(len(TokenType)+1)]
mark_literal[TokenType.PAREN_OPEN.value] = "("
mark_literal[TokenType.PAREN_CLOSE.value] = ")"
mark_literal[TokenType.EQUAL.value] = "="
mark_literal[TokenType.PLUS.value] = "+"
mark_literal[TokenType.MINUS.value] = "-"
mark_literal[TokenType.MULTIPLE.value] = "*"
mark_literal[TokenType.DIVISION.value] = "/"
mark_literal[TokenType.SINGLE_QUOTES.value] = "'"
mark_literal[TokenType.DOUBLE_QUOTES.value] = '"'
mark_literal[TokenType.BLANK.value] = " "
mark_literal[TokenType.BREAKLINE.value] = "\n"

keyword_literal : list[str] = ["" for i in range(len(TokenType)+1)]
keyword_literal[TokenType.PRINT.value] = "print"
keyword_literal[TokenType.WHILE.value] = "while"
keyword_literal[TokenType.IF.value] = "if"
keyword_literal[TokenType.JADOO.value] = "JADOO"
keyword_literal[TokenType.DOO.value] = "DOO"

@dataclass
class Token():
    """token class of jadoo lang"""

    def __post_init__(self):
        if mark_literal[self.type.value] != "":
            self.literal = mark_literal[self.type.value]
        elif keyword_literal[self.type.value] != "":
            self.literal = keyword_literal[self.type.value]

    type : TokenType = None
    literal : str = None
    value : any = None

# lexer
def lexer(line : str) -> list:
    """lexer of jadoo lang"""

    tokenized : list = []
    tmp : str = ""
    i = 0
    while i < len(line):
        if line[i] not in list(mark_literal):
            tmp += line[i]
            i += 1
            if i < len(line):
                continue

        if tmp == "": # type of line[i] is "mark"
            if line[i] == mark_literal[TokenType.DOUBLE_QUOTES.value]:
                tmptkn = Token(type=TokenType.DOUBLE_QUOTES)
                tokenized.append(tmptkn) # append opening DOUBLE_QUOTES to tokenized list
                i += 1
                while line[i] != mark_literal[TokenType.DOUBLE_QUOTES.value]:
                    tmp += line[i]
                    i += 1
                tmptkn = Token(type=TokenType.STRING, literal=tmp, value=str(tmp))
                tokenized.append(tmptkn) # append STRING to tokenized list
                tmptkn = Token(type=TokenType.DOUBLE_QUOTES)
                tokenized.append(tmptkn) # append closing DOUBLE_QUOTES to tokenized list
                tmp = ""
            else:
                for token_type in TokenType:
                    if line[i] == mark_literal[token_type.value]:
                        tmptkn = Token(type=token_type)
                        tokenized.append(tmptkn) # append token to tokenized list
                        break
            i += 1
            continue

        for token_type in TokenType:
            if tmp == keyword_literal[token_type.value]:
                tmptkn = Token(type=token_type)
                tokenized.append(tmptkn) # append token to tokenized list
                break
        else: # tmp is not keyword
            if tmp.isdigit():
                tmptkn = Token(type=TokenType.INTEGER, literal=tmp, value=int(tmp))
                tokenized.append(tmptkn) # append INT(non-negative integer) to tokenized list
            else:
                tmptkn = Token(type=TokenType.NONE, literal=tmp)
                tokenized.append(tmptkn) # append NONE to tokenized list
        tmp = ""
    return tokenized

with open("code.jadoo", "rt", encoding="utf8") as f:
    code_tokenized : list[Token] = []
    line_raw = f.readline()
    while line_raw:
        line_tokenized = lexer(line_raw)
        for tkn in line_tokenized:
            print(f"[<{tkn.literal}>, {tkn.type.name}]", end=", ")
            # print(f"<{tkn.literal}>", end=", ")
            code_tokenized.append(tkn)
        line_raw = f.readline()

# lexer
