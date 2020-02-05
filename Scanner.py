from tokentype import TokenType
from token import Token
from PyLox import error as lox_error

class Scanner(object):
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.current = 0
        self.start = 0 
        self.line  = 1
        self.token_dic = {
            "{" : TokenType.LEFT_BRACE,
            "}" : TokenType.RIGHT_BRACE,
            "(" : TokenType.LEFT_PAREN,
            ")" : TokenType.RIGHT_PAREN,
            "," : TokenType.COMMA,
            "." : TokenType.DOT,
            "-" : TokenType.MINUS,
            "+" : TokenType.PLUS,
            ";" : TokenType.SEMICOLON,
            "*" : TokenType.STAR
        }

    def advance(self):
        c = self.source[self.current]
        self.current += 1 
        return c 
    
    def addToken(self, type, literal = None):
        text = self.source[self.start : self.current]
        t = Token(type, text, literal, self.line)
        self.tokens.append(t)

    def scanToken(self):
        c = self.advance()

        if c in self.token_dic:
            self.addToken(self.token_dic[c])
        else:
            lox_error(self.line, "Unexpected character.")
    
    def isAtEnd(self):
        return self.current >= len(self.source)

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        t = Token(TokenType.EOF, "", None, self.line)
        self.tokens.append(t)

        return self.tokens

    

    