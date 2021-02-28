# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.


from lox.ast.token import Token
from lox.ast.grammer import VisitorInterface, Expr, Binary, Unary, Grouping, Literal
from typing import List


class ASTPrinter(VisitorInterface):

    def print(self, expr: Expr):
        return expr.accept(self)

    def visitBinary(self, expr: Binary):
        exprs = [expr.left, expr.right]
        return self.parenthesize(expr.operator.lexeme, exprs)

    def visitGrouping(self, expr: Grouping):
        return self.parenthesize("group", [expr.expression])

    def visitLiteral(self, expr: Literal):
        if expr.value == None:
            return "nil"
        return str(expr.value)

    def visitUnary(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, [expr.right])

    def parenthesize(self, name, exprs: List[Expr]):
        out = "(" + name

        for e in exprs:
            out += " "
            out += e.accept(self)

        out += ")"

        return out
