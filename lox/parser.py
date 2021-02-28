# Copyright (c) 2021 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.

from lox.ast.grammer import Expr, Binary, Unary, Grouping, Literal
from lox.ast.token import Token, TokenType
from lox.tools import logging as LoxLog
from typing import List, Union


class ParseError(Exception):
    """ This is a parsing error """
    pass


class Parser(object):
    """
    Parser Class get a list of tokens 
    and output AST
    """

    def __init__(self, tokens: List[Token]):
        self.tokens: List[Token] = tokens
        self.current: int = 0

    def parse(self) -> Union[Expr, None]:
        try:
            return self.expression()
        except ParseError:
            # TODO : Deal with the error
            print("Parse Error")
            return None

    def expression(self) -> Expr:
        """ Return the root of the (current sub-) AST 
            The rule: expression → equality
        """
        return self.equality()

    def equality(self) -> Expr:
        """equality → comparison ( ( "!=" | "==" ) comparison )* """
        expr = self.comparison()

        match_list = [TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]
        while self.match(match_list):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        """ comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ; """
        expr = self.term()

        # GREATER, GREATER_EQUAL, LESS, LESS_EQUAL
        match_list = [TokenType.GREATER, TokenType.GREATER_EQUAL,
                      TokenType.LESS, TokenType.LESS_EQUAL]
        while self.match(match_list):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        """ term → factor ( ( "-" | "+" ) factor )* ;"""

        expr = self.factor()

        # MINUS, PLUS
        match_list = [TokenType.MINUS, TokenType.PLUS]
        while self.match(match_list):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        """ factor → unary ( ( "/" | "*" ) unary )* ; """
        expr = self.unary()

        # SLASH / , STAR *
        match_list = [TokenType.SLASH, TokenType.STAR]
        while self.match(match_list):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        """ Rule: unary → ( "!" | "-" ) unary
                        | primary ;
        """

        #BANG, MINUS
        match_list = [TokenType.BANG, TokenType.MINUS]
        if self.match(match_list):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        """ Rule:  primary → NUMBER | STRING | "false" | "true" | "nil" | "(" expression ")" ; """

        if self.match([TokenType.FALSE]):
            return Literal(False)

        if self.match([TokenType.TRUE]):
            return Literal(True)

        if self.match([TokenType.NIL]):
            return Literal(None)

        # NUMBER, STRING
        if self.match([TokenType.NUMBER, TokenType.STRING]):
            value = self.previous().literal
            return Literal(value)

        if self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")

            return Grouping(expr)

        raise self.error(self.peek().type, "Expect expression.")

    def synchronize(self):
        """ TODO ???  """
        token_list = [TokenType.CLASS, TokenType.FUN, TokenType.VAR,
                      TokenType.FOR, TokenType.IF, TokenType.WHILE,
                      TokenType.PRINT, TokenType.RETURN]

        self.advance()

        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return

            t = self.peek().type
            if t in token_list:
                return

            self.advance()

    def consume(self, token_type: TokenType, error_message: str):
        """ Increase the current counter by 1 if the token_type is the same 
            as the current TokenType otherwise raise error with error_message
        """
        if self.check(token_type):
            return self.advance()

        raise self.error(token_type, error_message)

    def error(self, token_type: TokenType, message: str) -> ParseError:
        """ Log the parser error and return ParseError object """
        LoxLog.error_token(token_type, message)
        return ParseError()

    def match(self, match_list: List[TokenType]) -> bool:
        """ Return True if the current TokenType is in the input list of TokenTypes """
        for type in match_list:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType) -> bool:
        """ check if the given token_type is the same as the current token  """
        if self.isAtEnd():
            return False  # Todo : Is this nessary?

        return self.peek().type == token_type

    def advance(self) -> Token:
        """ Return current token and increase the current counter """
        if not self.isAtEnd():
            self.current += 1

        return self.previous()

    def peek(self) -> Token:
        """
            Return the current token 
            Does not effect the current counter
        """
        return self.tokens[self.current]

    def isAtEnd(self) -> bool:
        """ Return True if current TokenType is EOF (End Of File)"""
        return self.peek().type == TokenType.EOF

    def previous(self) -> Token:
        """ Get the previous token """
        return self.tokens[self.current - 1]
