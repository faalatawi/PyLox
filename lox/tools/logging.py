# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.

from lox.ast.token import Token, TokenType


def report(line: int, where: str, message: str):
    out = f"[line {line} ] Error {where} :  {message} "
    print(out)


def error_line(line: int, message: int):
    report(line, "", message)


def error_token(token: Token, message: str):
    if token.type == TokenType.EOF:
        report(token.line, "  at end", message)

    report(token.line, " at '" + token.lexeme + "'", message)


def error_runtime(token: Token, message: str):
    # FIXME
    report(token.line, " at '" + token.lexeme + "'", message)
