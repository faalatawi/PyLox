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
            "*" : TokenType.STAR,
            "!" : TokenType.BANG,
            "!=" : TokenType.BANG_EQUAL,
            "=" : TokenType.EQUAL,
            "==" : TokenType.EQUAL_EQUAL,
            "<" : TokenType.LESS,
            "<=" : TokenType.LESS_EQUAL,
            ">" : TokenType.GREATER,
            ">=" : TokenType.GREATER_EQUAL 
        }

    def advance(self):
        c = self.source[self.current]
        self.current += 1 
        return c 
    
    def addToken(self, type, literal = None):
        text = self.source[self.start : self.current]
        t = Token(type, text, literal, self.line)
        self.tokens.append(t)
    
    def match(self, expected):
        if self.isAtEnd() :
            return False
        elif self.source[self.current] != expected :
            return False
        
        self.current += 1
        return True

    def peek(self):
        if self.isAtEnd() :
            return "\0"
        return self.source[self.current]

    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        
        #Unterminated string.                                 
        if self.isAtEnd() :                                         
            lox_error(self.line, "Unterminated string.")              
            return

        # The closing ".
        self.advance()

        start = self.start + 1
        end = self.current - 1
        value = self.source[start:end] #TODO

        self.addToken(TokenType.STRING, value)                                              
    
    def isDigit(self, c):
        return '0' <= c <= '9'
    
    def peekNext(self):
        next = self.current + 1
        if next >= len(self.source):
            return '\0'
        return self.source[next]

    def number(self):
        while self.isDigit(self.peek()) :
            self.advance()
        
        if self.peek() == '.' and self.isDigit(self.peekNext()):
            # Consume the "."
            self.advance()
        
        while self.isDigit(self.peek()) :
            self.advance()
        
        start = self.start 
        end = self.current 
        value = self.source[start:end] #TODO

        value = float(value)
        self.addToken(TokenType.NUMBER, value)


    def scanToken(self):
        c = self.advance()

        if c in self.token_dic:
            if c in ['!', '=', '<', '>'] and self.match("="):
                c += '='
            self.addToken(self.token_dic[c])

        elif c == "/":
            if self.match("/") :
                while self.peek() != "\n" and not self.isAtEnd():
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)
        
        elif c in ['\r', ' ', '\t']:
            pass

        elif c == '\n':
            self.line += 1

        elif c == '"':
            self.string()

        elif self.isDigit(c):
            self.number()

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

    

    