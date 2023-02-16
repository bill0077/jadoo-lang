from dataclasses import dataclass
from enum import Enum, auto
import re

class token_type(Enum):
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

mark_literal : list[str] = ["" for i in range(len(token_type)+1)]
mark_literal[token_type.PAREN_OPEN.value] = "("
mark_literal[token_type.PAREN_CLOSE.value] = ")"
mark_literal[token_type.EQUAL.value] = "="
mark_literal[token_type.PLUS.value] = "+"
mark_literal[token_type.MINUS.value] = "-"
mark_literal[token_type.MULTIPLE.value] = "*"
mark_literal[token_type.DIVISION.value] = "/"
mark_literal[token_type.SINGLE_QUOTES.value] = "'"
mark_literal[token_type.DOUBLE_QUOTES.value] = '"'
mark_literal[token_type.BLANK.value] = " "
mark_literal[token_type.BREAKLINE.value] = "\n"

keyword_literal : list[str] = ["" for i in range(len(token_type)+1)]
keyword_literal[token_type.PRINT.value] = "print"
keyword_literal[token_type.WHILE.value] = "while"
keyword_literal[token_type.IF.value] = "if"
keyword_literal[token_type.JADOO.value] = "JADOO"
keyword_literal[token_type.DOO.value] = "DOO"

@dataclass
class token():
    def __post_init__(self):
        if mark_literal[self.type.value] != "":
            self.literal = mark_literal[self.type.value]
        elif keyword_literal[self.type.value] != "":
            self.literal = keyword_literal[self.type.value]

    type : token_type = None
    literal : str = None
    value : any = None

# tokenizer
def line_tokenizer(line : str) -> list:
    tokenized : list = []
    tmp : str = ""
    i = 0
    while i < len(line):
        if line[i] not in [mark_literal_ for mark_literal_ in mark_literal]:
            tmp += line[i]
            i += 1
            if i < len(line):
                continue

        if tmp == "": # type of line[i] is "mark"
            if line[i] == mark_literal[token_type.DOUBLE_QUOTES.value]:
                tmptkn = token(type=token_type.DOUBLE_QUOTES)
                tokenized.append(tmptkn) # append opening DOUBLE_QUOTES to tokenized list
                i += 1
                while line[i] != mark_literal[token_type.DOUBLE_QUOTES.value]:
                    tmp += line[i]
                    i += 1
                tmptkn = token(type=token_type.STRING, literal=tmp, value=str(tmp))
                tokenized.append(tmptkn) # append STRING to tokenized list
                tmptkn = token(type=token_type.DOUBLE_QUOTES)
                tokenized.append(tmptkn) # append closing DOUBLE_QUOTES to tokenized list
                tmp = ""
                i += 1
                continue
            else:
                for token_type_ in token_type:
                    if line[i] == mark_literal[token_type_.value]:
                        tmptkn = token(type=token_type_)
                        tokenized.append(tmptkn) # append token to tokenized list
                        break
                i += 1
                continue

        for token_type_ in token_type:
            if tmp == keyword_literal[token_type_.value]:
                tmptkn = token(type=token_type_)
                tokenized.append(tmptkn) # append token to tokenized list
                break
        else: # tmp is not keyword
            if tmp.isdigit():
                tmptkn = token(type=token_type.INTEGER, literal=tmp, value=int(tmp))
                tokenized.append(tmptkn) # append INT(non-negative integer) to tokenized list
            else:    
                tmptkn = token(type=token_type.NONE, literal=tmp)
                tokenized.append(tmptkn) # append NONE to tokenized list
        tmp = ""
    return tokenized

with open("code.jadoo", "rt") as f:
    code_tokenized : list[token] = []
    line = f.readline()
    while line:
        line_tokenized = line_tokenizer(line)
        for tkn in line_tokenized:
            print(f"[<{tkn.literal}>, {tkn.type.name}]", end=", ")
            # print(f"<{tkn.literal}>", end=", ")
            code_tokenized.append(tkn)
        line = f.readline()

# lexer