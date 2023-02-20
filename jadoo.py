'''module for jadoo lang'''
from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    '''token type of jadoo lang'''
    # mark
    PAREN_OPEN = auto()
    PAREN_CLOSE = auto()
    EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLE = auto()
    DIVISION = auto()
    DOUBLE_QUOTES = auto()
    BLANK = auto()
    BREAKLINE = auto()

    # data type
    INTEGER = auto()
    STRING = auto()
    EXPRESSION = auto()

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
    ROOT = auto()

mark_literal : list[str] = ["" for i in range(len(TokenType)+1)]
mark_literal[TokenType.PAREN_OPEN.value] = "("
mark_literal[TokenType.PAREN_CLOSE.value] = ")"
mark_literal[TokenType.EQUAL.value] = "="
mark_literal[TokenType.PLUS.value] = "+"
mark_literal[TokenType.MINUS.value] = "-"
mark_literal[TokenType.MULTIPLE.value] = "*"
mark_literal[TokenType.DIVISION.value] = "/"
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
    '''token class of jadoo lang'''
    def __post_init__(self):
        if mark_literal[self.type.value] != "":
            self.literal = mark_literal[self.type.value]
        elif keyword_literal[self.type.value] != "":
            self.literal = keyword_literal[self.type.value]

    type : TokenType = TokenType.NONE
    literal : str = None
    value : any = None

def lexer(line : str) -> list[Token]:
    '''lexer of jadoo lang'''
    tokenized : list[Token] = []
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
                i += 1
                continue
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

def trimmer(tokenized : list[Token]) -> list[Token]:
    '''trimmer of jadoo lang'''
    trimmed : list[Token] = []
    for tkn in tokenized:
        if tkn.type == TokenType.BLANK:
            continue
        if tkn.type == TokenType.BREAKLINE:
            continue
        if tkn.type == TokenType.DOUBLE_QUOTES:
            continue
        trimmed.append(tkn)
    return trimmed

@dataclass
class ParseNode:
    '''node in parse tree of jadoo lang'''
    def __post_init__(self):
        self.parent : ParseNode = None
        self.child : list[ParseNode] = []

        if mark_literal[self.type.value] != "":
            self.literal = mark_literal[self.type.value]
        elif keyword_literal[self.type.value] != "":
            self.literal = keyword_literal[self.type.value]

    type : TokenType = TokenType.NONE
    literal : str = None
    value : any = None

@dataclass
class ParseTree:
    '''parse tree of jadoo lang'''
    def __post_init__(self):
        self.node_root : ParseNode = ParseNode(type=TokenType.ROOT)
        self.node_curr : ParseNode = self.node_root
        self.tkn_list : list[Token] = []
        self.tkn_curr : int = 0

    def print(self, node : ParseNode, indent : int = 0) -> None:
        '''print node in parse tree'''
        if node:
            for i in range(indent):
                print("    ", end="")
            print(f"[<{node.literal}>, {node.type.name}]")
            for child_ in node.child:
                self.print(child_, indent + 1)

    # currently working
    ###########################################################
    def parse(self, node: ParseNode) -> any:
        '''parser for jadoo lang'''
        if self.tkn_curr >= len(self.tkn_list):
            return
        
        tkn = self.tkn_list[self.tkn_curr]
        if tkn.type == TokenType.PRINT:
            tmpnode = ParseNode(type=TokenType.PRINT)
            tmpnode.parent = node
            node.child.append(tmpnode)
            self.tkn_curr += 1
            self.parse(tmpnode)
        elif tkn.type == TokenType.PAREN_OPEN:
            tmpnode = ParseNode(type=TokenType.PAREN_OPEN)
            tmpnode.parent = node
            node.child.append(tmpnode)
            self.tkn_curr += 1
            self.parse(node)
        elif tkn.type == TokenType.PAREN_CLOSE:
            tmpnode = ParseNode(type=TokenType.PAREN_CLOSE)
            tmpnode.parent = node
            node.child.append(tmpnode)
            self.tkn_curr += 1
            self.parse(node)
        elif tkn.type == TokenType.STRING:
            tmpnode = ParseNode(type=TokenType.STRING, literal=tkn.literal, value=tkn.value)
            tmpnode.parent = node
            node.child.append(tmpnode)
            self.tkn_curr += 1
            self.parse(node)
        elif tkn.type == TokenType.INTEGER:
            tmpnode = ParseNode(type=TokenType.INTEGER, literal=tkn.literal, value=tkn.value)
            tmpnode.parent = node
            node.child.append(tmpnode)
            self.tkn_curr += 1
            self.parse(node)

def print_parsetree_test():
    '''test printng fuction of parse tree'''
    print("testing parsetree print func : ")
    testtree = ParseTree()
    tmpnode1 = ParseNode(type=TokenType.PRINT)
    tmpnode1.parent = testtree.node_root
    testtree.node_root.child.append(tmpnode1)
    tmpnode2 = ParseNode(type=TokenType.PAREN_OPEN)
    tmpnode2.parent = tmpnode1
    tmpnode1.child.append(tmpnode2)
    tmpnode3 = ParseNode(type=TokenType.EXPRESSION)
    tmpnode3.parent = tmpnode1
    tmpnode1.child.append(tmpnode3)
    tmpnode4 = ParseNode(type=TokenType.INTEGER)
    tmpnode4.parent = tmpnode3
    tmpnode3.child.append(tmpnode4)
    tmpnode5 = ParseNode(type=TokenType.PLUS)
    tmpnode5.parent = tmpnode3
    tmpnode3.child.append(tmpnode5)
    tmpnode6 = ParseNode(type=TokenType.INTEGER)
    tmpnode6.parent = tmpnode3
    tmpnode3.child.append(tmpnode6)
    tmpnode7 = ParseNode(type=TokenType.PAREN_CLOSE)
    tmpnode7.parent = tmpnode1
    tmpnode1.child.append(tmpnode7)
    testtree.print(testtree.node_root)

def parser(trimmed : list[TokenType]) -> dict:
    '''parser for jadoo lang'''
    parsetree = ParseTree()
    parsetree.tkn_list = trimmed
    parsetree.parse(parsetree.node_root)
    parsetree.print(parsetree.node_root)

if __name__ == "__main__":
    with open("code.jadoo", "rt", encoding="utf8") as f:
        code_tokenized : list[Token] = []
        line_raw = f.readline()
        while line_raw:
            for i in range(100):
                print("=", end="")
            print(f"\n\nline : <{line_raw.strip()}>", end="")

            print("\n\nlexer : ", end="")
            line_tokenized = lexer(line_raw)
            for token in line_tokenized:
                print(f"[<{token.literal}>, {token.type.name}]", end=", ")

            print("\n\ntrimmer : ", end="")
            line_trimmed = trimmer(line_tokenized)
            for token in line_trimmed:
                print(f"[<{token.literal}>, {token.type.name}]", end=", ")
                # print(f"<{tkn.literal}>", end=", ")
                code_tokenized.append(token)
            print("\n\n", end="")
            line_raw = f.readline()

            print("parser : ")
            parser(code_tokenized)
            # print_parsetree_test()
            # code_parsed = parse_tree.build_dict(parse_tree.node_root)
            # print(code_parsed)
            # (/・・)ノ. (ﾉ・ｪ・)ﾉ.
