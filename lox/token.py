# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.

class Token(object):
    
    def __init__(self, type,  lexeme,  literal,  line):
        self.type = type
        self.lexeme = lexeme 
        self.literal = literal
        self.line = line
    
    def __str__(self):
        return f"Token [type : {self.type}, lexeme: {self.lexeme} literal : {self.literal}, line : {self.line}]"
