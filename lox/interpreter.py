# Copyright (c) 2021 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.

from ast.grammer import VisitorInterface, Expr, Binary, Unary, Grouping, Literal
from ast.token import Token, TokenType
from tools import logging as LoxLog
from typing import Union, Any


class RuntimeError(Exception):
    """This is a RuntimeError error"""

    def __init__(self, token: Token, message: str):
        self.message = message
        self.token = token

    def __str__(self):
        return f"RuntimeError: {self.message} , token = {self.token} "


class Interpreter(VisitorInterface):

    def interpret(self, expr: Expr) -> Union[float, str]:
        """ Use this function to interpret and AST """
        try:
            value = self.evaluate(expr)
            return value
        except RuntimeError as e:
            # TODO: How to handdel this type of errors
            LoxLog.error_runtime(e.token, e.message)

    def evaluate(self, expr: Expr) -> Union[float, str, bool, None]:
        return expr.accept(self)

    def visitLiteral(self, expr: Literal) -> Union[float, str]:
        return expr.value

    def visitGrouping(self, expr: Grouping) -> Union[float, str, bool, None]:
        return self.evaluate(expr.expression)

    def visitUnary(self, expr: Unary) -> Union[float, str, bool, None]:
        right = self.evaluate(expr.right)
        op_type = expr.operator.type

        if op_type == TokenType.MINUS:
            # Raise error if right not a number
            self.checkNumberOperand(expr.operator, right)
            return -1 * float(right)

        if op_type == TokenType.BANG:
            return not self.isTruthy(right)

        # Unreachable
        return None

    def visitBinary(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        op_type = expr.operator.type

        if op_type == TokenType.MINUS:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) - float(right)

        if op_type == TokenType.SLASH:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) / float(right)

        if op_type == TokenType.STAR:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) * float(right)

        if op_type == TokenType.PLUS:
            if (type(left) == float) and (type(right) == float):
                return left + right

            if (type(left) == str) and (type(right) == str):
                return left + right

            raise RuntimeError(
                expr.operator, "Operands must be two numbers or two strings.")

        if op_type == TokenType.GREATER:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) > float(right)

        if op_type == TokenType.GREATER_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) >= float(right)

        if op_type == TokenType.LESS:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) < float(right)

        if op_type == TokenType.LESS_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) <= float(right)

        if op_type == TokenType.BANG_EQUAL:
            return not self.isEqual(left, right)

        if op_type == TokenType.EQUAL_EQUAL:
            return self.isEqual(left, right)

        return None

    def isTruthy(self, expr: Union[bool, None, Any]) -> bool:
        if expr == None:
            return False

        if type(expr) == bool:
            return expr

        return True

    def isEqual(self, left, right) -> bool:
        return left == right

    def checkNumberOperand(self, operator: Token, operand: Union[float, str, bool, None]):
        """ Raise an error if the operand is not a number """
        if type(operand) == float:
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def checkNumberOperands(self, operator: Token, left: Union[float, str, bool, None], right: Union[float, str, bool, None]):
        """ Raise an error if left or right are not a number """
        if type(left) == float and type(right) == float:
            return
        raise RuntimeError(operator, "Operands must be a number.")
