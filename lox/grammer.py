# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file. 

class Expr:
    pass

class VisitorInterface:
	def visitBinary(self, expr):
		pass
	def visitGrouping(self, expr):
		pass
	def visitLiteral(self, expr):
		pass
	def visitUnary(self, expr):
		pass


class Binary(Expr):
	def __init__(self, left, operator, right):
		self.left = left 
		self.operator = operator 
		self.right = right 

	def accept(self, visitor):
		return visitor.visitBinary(self)


class Grouping(Expr):
	def __init__(self, expression):
		self.expression = expression 

	def accept(self, visitor):
		return visitor.visitGrouping(self)


class Literal(Expr):
	def __init__(self, value):
		self.value = value 

	def accept(self, visitor):
		return visitor.visitLiteral(self)


class Unary(Expr):
	def __init__(self, operator, right):
		self.operator = operator 
		self.right = right 

	def accept(self, visitor):
		return visitor.visitUnary(self)
