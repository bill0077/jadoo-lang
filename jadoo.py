from dataclasses import dataclass

code : str = input()

code_list = list(code)

token : list[str] = ["jadoo", "doo", "print", "while", "if", "(", ")", "+", "-", "*", "/", " "]

@dataclass
class token:
    type : str = None
    literal : str = None
    length : int = None

BRACKET_OPEN = token(type="sign", literal="(", length=1)
BRACKET_CLOSE = token(type="sign", literal=")", length=1)
PLUS = token(type="sign", literal="+", length=1)
MINUS = token(type="sign", literal="-", length=1)
MULTIPLE = token(type="sign", literal="*", length=1)
DIVISION = token(type="sign", literal="/", length=1)
BLANK = token(type="sign", literal=" ", length=1)
JADOO = token(type="reserved_word", literal="jadoo", length=5)
DOO = token(type="reserved_word", literal="doo", length=3)
PRINT = token(type="reserved_word", literal="print", length=5)
WHILE = token(type="reserved_word", literal="while", length=5)
IF = token(type="reserved_word", literal="if", length=2)
NONE = token(type="none", literal="", length=0)

token_list : list = [
    BRACKET_OPEN,
    BRACKET_CLOSE,
    PLUS,
    MINUS,
    MULTIPLE,
    DIVISION,
    BLANK,
    JADOO,
    DOO,
    PRINT,
    WHILE,
    IF,
    NONE
]

# tokenizer
def get_token(line : str):
    tokenized : list = []
    tmp : str = ""
    i = 0
    while i < len(line):
        if line[i] not in ["(", ")", "+", "-", "*", "/", " "]:
            tmp += line[i]
            i += 1
        else:
            if tmp == "":
                tmp = line[i]
                i += 1
            tokenized.append(NONE)
            for token_ in token_list:
                if tmp == token_.literal:
                    tokenized.pop()
                    tokenized.append(token_)
                    break
            tmp = ""
    if tmp != "":
        tokenized.append(NONE)
        for token_ in token_list:
            if tmp == token_.literal:
                tokenized.pop()
                tokenized.append(token_)
                break
    return tokenized

for a in get_token(code):
    print(f"[{a.literal}]", end=", ")

print("done")