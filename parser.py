import sys
from lexer import Lexer
from token_ import Token, TokenKind
from node_ import BinaryNode, CompoundNode, IfNode, Node, UnaryNode

class Parser:
	lexer: Lexer
	current: Token|None

	def __init__(self, lexer: Lexer):
		self.current = None
		self.lexer = lexer

	def next(self) -> Token|None:
		self.current = self.lexer.lex()
		return self.current

	def parse(self) -> Node|None:
		self.next()
		if not self.current: return

		node = CompoundNode([])

		while self.current.kind != TokenKind.EOI:
			expr = self.stmt()
			if not expr: return
			node.body.append(expr)

		return node

	def compound(self) -> Node|None:
		if not self.current: return

		if self.current.kind != TokenKind.OpenBrace:
			print(f'Expected opening brace at {self.current.start}', file=sys.stderr)
			return

		self.next()
		node = CompoundNode([])

		while self.current and self.current.kind not in (TokenKind.EOI, TokenKind.CloseBrace):
			expr = self.stmt()
			if not expr: return
			node.body.append(expr)

		if self.current.kind != TokenKind.CloseBrace:
			print(f'Expected closing brace at {self.current.start}', file=sys.stderr)
			return

		self.next()
		return node

	def stmt(self) -> Node|None:
		if not self.current: return

		if self.current.kind == TokenKind.If:
			self.next()

			cmp = self.logic()
			if not cmp: return

			body = self.compound()
			if not body: return

			node = IfNode(cmp, body, None)
			last_node = node

			while self.current.kind == TokenKind.Elsif:
				self.next()

				cmp = self.logic()
				if not cmp: return

				body = self.compound()
				if not body: return

				last_node.else_ = IfNode(cmp, body, None)
				last_node = last_node.else_

			if self.current.kind == TokenKind.Else:
				self.next()
				body = self.compound()
				if not body: return
				last_node.else_ = body

			return node
		elif self.current.kind in (TokenKind.Elsif, TokenKind.Else):
			print(f'Unexpected {self.current.kind} at {self.current.start}', file=sys.stderr)
		else:
			return self.logic()

	def logic(self) -> Node|None:
		lhs = self.cmp()
		if not lhs: return

		while self.current and self.current.kind in (TokenKind.LogicAnd, TokenKind.LogicOr):
			op = self.current
			self.next()
			rhs = self.cmp()
			if not rhs: return
			lhs = BinaryNode(lhs, op, rhs)

		return lhs

	def cmp(self) -> Node|None:
		lhs = self.add()
		if not lhs: return

		while self.current and self.current.kind in (TokenKind.Equal, TokenKind.Diff, TokenKind.Less, TokenKind.LessEqual, TokenKind.Greater, TokenKind.GreaterEquals):
			op = self.current
			self.next()
			rhs = self.add()
			if not rhs: return
			lhs = BinaryNode(lhs, op, rhs)

		return lhs

	def add(self) -> Node|None:
		lhs = self.multiply()
		if not lhs: return

		while self.current and self.current.kind in (TokenKind.Plus, TokenKind.Minus):
			op = self.current
			self.next()
			rhs = self.multiply()
			if not rhs: return
			lhs = BinaryNode(lhs, op, rhs)

		return lhs

	def multiply(self) -> Node|None:
		lhs = self.unary()
		if not lhs: return

		while self.current and self.current.kind in (TokenKind.Multiply, TokenKind.Divide):
			op = self.current
			self.next()
			rhs = self.unary()
			if not rhs: return
			lhs = BinaryNode(lhs, op, rhs)

		return lhs

	def unary(self) -> Node|None:
		if not self.current: return

		if self.current.kind == TokenKind.Minus:
			op = self.current
			self.next()
			expr = self.factor()
			if not expr: return
			return UnaryNode(expr, op)
		else:
			return self.factor()

	def factor(self) -> Node|None:
		if not self.current: return

		match self.current.kind:
			case TokenKind.Ident | TokenKind.Integer | TokenKind.Float | TokenKind.String | TokenKind.Char:
				token = self.current
				self.next()
				return token

			case TokenKind.OpenParen:
				self.next()
				expr = self.logic()

				if self.current.kind != TokenKind.CloseParen:
					print(f'Expected closing parenthesis at {self.current.start}', file=sys.stderr)
					return

				self.next()
				return expr

			case TokenKind.OpenBrace:
				return self.compound()

			case _:
				print(f'Unexpected token {self.current} in factor consumer', file=sys.stderr)
