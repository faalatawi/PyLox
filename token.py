class Token(object):
    
    def __init__(self, type,  lexeme,  literal,  line):
        self.type = type
        self.lexeme = lexeme 
        self.literal = literal
        self.line = line
    
    def to_str(self):
        return str(self.type) + " " + str(self.literal) + " " + str(self.line) 