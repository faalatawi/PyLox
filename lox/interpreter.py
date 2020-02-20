# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.

from . import grammer
from .token_type import TokenType

class Interpreter(grammer.VisitorInterface):
    def __init__(self):
        print("test")
    def evaluate(self, expr):
        return expr.accept(self)

    def visitLiteral(self, expr : grammer.Literal):
        return expr.value 
    
    def visitGrouping(self, expr : grammer.Grouping):
        return self.evaluate(expr.expression)
    
    def visitUnary(self, expr : grammer.Unary):
        right = self.evaluate(expr.right)

        if expr.operator == TokenType.MINUS :
            return -1 * float(right)
        
        if expr.operator == TokenType.BANG :
            return not self._is_truthy(right)

        # Unreachable
        return None
    
    
    def visitBinary(self, expr : grammer.Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator == TokenType.MINUS:
            return float(left) - float(right)
        
        if expr.operator == TokenType.SLASH :
            return float(left) / float(right)
        
        if expr.operator == TokenType.STAR :
            return float(left) * float(right)

        if expr.operator == TokenType.PLUS :
            if ( type(left) == float ) and ( type(right) == float ):
                return left + right

            if ( type(left) == str ) and ( type(right) == str ):
                return left + right
        
        if expr.operator == TokenType.GREATER :
            return float(left) > float(right)

        if expr.operator == TokenType.GREATER_EQUAL :
            return float(left) >= float(right)

        if expr.operator == TokenType.LESS :
            return float(left) < float(right)
        
        if expr.operator == TokenType.LESS_EQUAL :
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
