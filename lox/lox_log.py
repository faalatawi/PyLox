# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.
 

from lox.token_type import TokenType
from termcolor import colored

def report(line, where, message):
    out = f"[line {line} ] Error {where} :  {message} "
    # print(colored(out, 'red'))
    print(out)

def error_line(line, message):
    report(line, "", message)

def error_token(token, message):
    if token == TokenType.EOF :
        report(token.line, "  at end", message)
    
    report(token.line, " at '" + token.lexeme + "'", message)