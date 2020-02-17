# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.

from lox import grammer
from lox.token_type import TokenType
import lox.lox_log as LoxLog 
from lox.token import Token 

class ParseError(Exception):
    """This is a parsing error"""
    pass 


class Parser(object):
    
    def __init__(self, tokens):
        self._tokens  = tokens
        self._current = 0
    
    def parse(self):
        try : 
            return self._expression()
        except ParseError:
            print("ParseError")
            return None
    
    def _expression(self):
        return self._equality()

    def _equality(self):
        """equality → comparison ( ( "!=" | "==" ) comparison )* """
        expr = self._comparison()

        match_list = [TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]
        while self._match(match_list) : 
            operator = self._previous()
            right = self._comparison()
            expr = grammer.Binary(expr, operator, right)
        
        return expr
    
    # comparison → addition ( ( ">" | ">=" | "<" | "<=" ) addition )* ;
    def _comparison(self):
        expr = self._addition()

        # GREATER, GREATER_EQUAL, LESS, LESS_EQUAL
        match_list = [TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL]
        while self._match(match_list) : 
            operator = self._previous()
            right = self._addition()
            expr = grammer.Binary(expr, operator, right)
        
        return expr
    
    def _addition(self):
        expr = self._multiplication()

        # MINUS, PLUS
        match_list = [TokenType.MINUS, TokenType.PLUS]
        while self._match(match_list) : 
            operator = self._previous()
            right = self._multiplication()
            expr = grammer.Binary(expr, operator, right)
        
        return expr
    
    def _multiplication(self):
        expr = self._unary()

        # SLASH, STAR
        match_list = [TokenType.SLASH, TokenType.STAR]
        while self._match(match_list):
            operator = self._previous()
            right = self._unary()
            expr = grammer.Binary(expr, operator, right)
        
        return expr

    # unary → ( "!" | "-" ) unary
    #       | primary ;
    def _unary(self):
        #BANG, MINUS
        match_list = [TokenType.BANG, TokenType.MINUS]
        if self._match(match_list):
            operator = self._previous()
            right = self._unary()
            return grammer.Unary(operator, right)
        
        return self._primary()

    # primary → NUMBER | STRING | "false" | "true" | "nil" | "(" expression ")" ;
    def _primary(self):

        if self._match([TokenType.FALSE]):
            return grammer.Literal(False)
        
        if self._match([TokenType.TRUE]):
            return grammer.Literal(True)
        
        if self._match([TokenType.NIL]):
            return grammer.Literal(None)
        
        # NUMBER, STRING
        if self._match([TokenType.NUMBER, TokenType.STRING]):
            value = self._previous().literal
            return grammer.Literal(value)

        
        if self._match([TokenType.LEFT_PAREN]) : 
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")

            return grammer.Grouping(expr)

        raise self._error(self._peek(), "Expect expression.")
    
    def _synchronize(self):
        token_list = [TokenType.CLASS, TokenType.FUN, TokenType.VAR,
                    TokenType.FOR, TokenType.IF, TokenType.WHILE,
                    TokenType.PRINT, TokenType.RETURN]

        self._advance()

        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return

            t = self._peek().type
            if t in token_list:
                return
            
            self._advance()

    # ===================================================
    # Helping methods 

    def _consume(self, token, message):
        if self._check(token):
            return self._advance()
        
        raise self._error(token, message)

    def _error(self, token, message):
        LoxLog.error_token(token, message) 

        return ParseError()

    def _match(self, match_list) -> bool:
        for _type in match_list:
            if self._check(_type) :
                self._advance()
                return True
        
        return False

    def _check(self, token) -> bool:
        if self._is_at_end():
            return False
        
        return self._peek().type == token

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._current += 1

        return self._previous()    

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]


# test
if __name__ == "__main__":
    
    import scanner 

    source = ""

    lox_scan = scanner.Scanner(source)

    tokens = lox_scan.scanTokens()

    print("==> Tokens:")
    for t in tokens:
        print(t)
    print("\n\n")

    lox_parser = Parser(tokens)
    result = lox_parser.parse()

    import ast_printer

    printer = ast_printer.ASTPrinter()

    print(printer.print(result))