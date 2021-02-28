# Copyright (c) 2021 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.

from typing import Union
from lox.ast.token import Token 

class Expr(object):
    def accept(self, visitor):
        pass


class VisitorInterface(object):
	def visitBinary(self, expr):
		pass
	def visitGrouping(self, expr):
		pass
	def visitLiteral(self, expr):
		pass
	def visitUnary(self, expr):
		pass

class Binary(Expr):
	def __init__(self, left : Expr, operator : Token, right : Expr):
		self.left : Expr = left 
		self.operator : Token = operator 
		self.right : Expr = right 

	def accept(self, visitor : VisitorInterface):
		return visitor.visitBinary(self)

class Grouping(Expr):
	def __init__(self, expression : Expr):
		self.expression : Expr = expression 

	def accept(self, visitor : VisitorInterface):
		return visitor.visitGrouping(self)

class Literal(Expr):
	def __init__(self, value : Union[float, str]):
		self.value : Union[float, str] = value 

	def accept(self, visitor : VisitorInterface):
		return visitor.visitLiteral(self)

class Unary(Expr):
	def __init__(self, operator : Token, right : Expr):
		self.operator : Token = operator 
		self.right : Expr = right 

	def accept(self, visitor : VisitorInterface):
		return visitor.visitUnary(self)
