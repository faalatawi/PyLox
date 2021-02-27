# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.


import lox.ast.grammer as grammer
from lox.ast.token import Token


class ASTPrinter(grammer.VisitorInterface):

    def print(self, expr):
        return expr.accept(self)

    def visitBinary(self, expr: grammer.Binary):
        exprs = [expr.left, expr.right]
        return self._parenthesize(expr.operator.lexeme, exprs)

    def visitGrouping(self, expr: grammer.Grouping):
        return self._parenthesize("group", [expr.expression])

    def visitLiteral(self, expr: grammer.Literal):
        if expr.value == None:
            return "nil"
        return str(expr.value)

    def visitUnary(self, expr: grammer.Unary):
        return self._parenthesize(expr.operator.lexeme, [expr.right])

    def _parenthesize(self, name, exprs):
        out = "(" + name

        for e in exprs:
            out += " "
            out += e.accept(self)

        out += ")"

        return out


# Testing
if __name__ == "__main__":

    from token_type import TokenType as TT

    expression = grammer.Binary(
        left=grammer.Unary(
            operator=Token(TT.MINUS, "-", None, 1),
            right=grammer.Literal(123)
        ),
        operator=Token(TT.STAR, "*", None, 1),
        right=grammer.Grouping(
            expression=grammer.Literal(45.67)
        )

    )

    print(ASTPrinter().print(expression))
