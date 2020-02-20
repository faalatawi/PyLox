# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.

from . import grammer
from .token_type import TokenType
from . import lox_log

class RuntimeError(Exception):
    """This is a RuntimeError error"""

    def __init__(self, token : TokenType, message):
        self.message = message 
        self.token = token
    
    def __str__(self):
        return f"RuntimeError: {self.message} , token = {self.token} "


class Interpreter(grammer.VisitorInterface):
    def __init__(self):
        print("test")

    def interpret(self, expr):
        try:
            value = self.evaluate(expr)
        except RuntimeError as e:
            pass

        

    def evaluate(self, expr):
        return expr.accept(self)

    def visitLiteral(self, expr : grammer.Literal):
        return expr.value 
    
    def visitGrouping(self, expr : grammer.Grouping):
        return self.evaluate(expr.expression)
    
    def visitUnary(self, expr : grammer.Unary):
        right = self.evaluate(expr.right)

        if expr.operator == TokenType.MINUS :
            self._check_number_operand(expr.operator, right)
            return -1 * float(right)
        
        if expr.operator == TokenType.BANG :
            return not self._is_truthy(right)

        # Unreachable
        return None
    
    
    def visitBinary(self, expr : grammer.Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator == TokenType.MINUS:
            self._check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        
        if expr.operator == TokenType.SLASH :
            self._check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        
        if expr.operator == TokenType.STAR :
            self._check_number_operands(expr.operator, left, right)
            return float(left) * float(right)

        if expr.operator == TokenType.PLUS :
            if ( type(left) == float ) and ( type(right) == float ):
                return left + right

            if ( type(left) == str ) and ( type(right) == str ):
                return left + right
            
            raise RuntimeError(expr.operator, "Operands must be two numbers or two strings.")
        
        if expr.operator == TokenType.GREATER :
            self._check_number_operands(expr.operator, left, right)
            return float(left) > float(right)

        if expr.operator == TokenType.GREATER_EQUAL :
            self._check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)

        if expr.operator == TokenType.LESS :
            self._check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        
        if expr.operator == TokenType.LESS_EQUAL :
            self._check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        
        if expr.operator == TokenType.BANG_EQUAL :
            return not self._is_equal(left, right)
        
        if expr.operator == TokenType.EQUAL_EQUAL :
            return self._is_equal(left, right)

        return None


    # ======
    def _is_truthy(self, expr):
        if expr == None:
            return False
        
        if type(expr) == bool :
            return expr
        
        return True
    
    def _is_equal(self, left, right):
        # NO NEED: 
        # if left == None and right == None:
        #     return True
        # if left == None :
        #     return False 
        return left == right

    def _check_number_operand(self, operator : TokenType, operand):
        if type(operand) == float :
            return
        raise RuntimeError(operator, "Operand must be a number.") 

    def _check_number_operands(self, operator, left, right):
        if type(left) == float and type(right) == float :
            return
        raise RuntimeError(operator, "Operands must be a number.") 
