# Copyright (c) 2021 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.

from lox.ast.token import TokenType, Token, lox_keywords, lox_token_dic
import lox.tools.logging as LoxLog
from typing import List, Union


class Scanner(object):
    def __init__(self, source: str):
        self.source: str = source
        self.tokens: List[Token] = []
        self.current: int = 0
        self.start: int = 0
        self.line: int = 1

        # For optimization:
        self.len_of_source: int = len(self.source)

    def advance(self) -> str:
        """ Get the current char and advance to the next """
        c = self.source[self.current]
        self.current += 1
        return c

    def addToken(self, type: TokenType, literal: Union[float, str] = None):
        """ Add a token to tokens list """
        text = self.source[self.start: self.current]
        t = Token(type, text, literal, self.line)
        self.tokens.append(t)

    def match(self, expected: str) -> bool:
        """ Match the input char with the current char and advance current counter """
        if self.isAtEnd():
            return False
        elif self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        """ Return the current char without chaning the current counter """
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]

    def string(self):
        """ Add a string token to tokens list """
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        # Unterminated string.
        if self.isAtEnd():
            LoxLog.error_line(self.line, "Unterminated string.")
            return

        # The closing ".
        self.advance()

        start = self.start + 1
        end = self.current - 1
        value = self.source[start:end]

        self.addToken(TokenType.STRING, value)

    def isDigit(self, c) -> bool:
        """ Return True if c is a digit and False otherwise """
        return '0' <= c <= '9'

    def peekNext(self) -> str:
        """ Peek into the next char without increasing current counter """
        next = self.current + 1
        if next >= self.len_of_source:
            return '\0'
        return self.source[next]

    def number(self):
        """ Add a number token to tokens list"""

        while self.isDigit(self.peek()):
            self.advance()

        if self.peek() == '.' and self.isDigit(self.peekNext()):
            # Consume the "."
            self.advance()

        while self.isDigit(self.peek()):
            self.advance()

        start = self.start
        end = self.current
        value = self.source[start:end]

        value = float(value)
        self.addToken(TokenType.NUMBER, value)

    def isAlpha(self, c: str) -> bool:
        """ Is this char is Alpha """
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_'

    def isAlphaNumeric(self, c) -> bool:
        return self.isAlpha(c) or self.isDigit(c)

    def identifier(self):
        """ Add a identifier token to tokens list"""

        while self.isAlphaNumeric(self.peek()):
            self.advance()

        start = self.start
        end = self.current
        value = self.source[start:end]

        if value in lox_keywords:
            self.addToken(lox_keywords[value])
        else:
            self.addToken(TokenType.IDENTIFIER, value)

    def scanToken(self):
        """ Scan one token from source string  """

        c = self.advance()

        if c in lox_token_dic:
            if c in ['!', '=', '<', '>'] and self.match("="):
                c += '='
            self.addToken(lox_token_dic[c])

        elif c == "/":
            if self.match("/"):
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

        elif self.isAlpha(c):
            self.identifier()

        else:
            LoxLog.error_line(self.line, "Unexpected character. : " + c)

    def isAtEnd(self) -> bool:
        """ Are we at the end of the source?  """
        return self.current >= self.len_of_source

    def scanTokens(self) -> List[Token]:
        """ Scan all the tokens in source string  """

        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        t = Token(TokenType.EOF, "", None, self.line)
        self.tokens.append(t)

        return self.tokens
