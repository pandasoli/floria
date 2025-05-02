import sys
from typing import Callable, Dict
from lexer import Lexer
from token_ import Token, TokenKind
from node import BinaryNode, CompoundNode, IfNode, LiteralNode, Node, UnaryNode

class Parser:
	lexer: Lexer
	current: Token|None
	PRECEDENCE: Dict[TokenKind, int]
	prefix_parselets: Dict[TokenKind, Callable[[], Node|None]]
	infix_parselets: Dict[TokenKind, Callable]

	def __init__(self, lexer: Lexer):
		self.current = None
		self.lexer = lexer

		self.PRECEDENCE = {
			TokenKind.LogicOr: 1,
			TokenKind.LogicAnd: 2,
			TokenKind.Equal: 3,
			TokenKind.Diff: 3,
			TokenKind.Less: 4,
			TokenKind.LessEqual: 4,
			TokenKind.Greater: 4,
			TokenKind.GreaterEquals: 4,
			TokenKind.Plus: 5,
			TokenKind.Minus: 5,
			TokenKind.Multiply: 6,
			TokenKind.Divide: 6,
			TokenKind.Mod: 6,
			TokenKind.Pow: 7
		}

		self.prefix_parselets = {
			TokenKind.Ident: self.parse_literal,
			TokenKind.Integer: self.parse_literal,
			TokenKind.Float: self.parse_literal,
			TokenKind.String: self.parse_literal,
			TokenKind.Char: self.parse_literal,
			TokenKind.Minus: self.parse_prefix,
			TokenKind.Plus: self.parse_prefix,
			TokenKind.OpenParen: self.parse_group,
			TokenKind.If: self.parse_if,
			TokenKind.OpenBrace: self.parse_compound
		}

		self.infix_parselets = {
			TokenKind.Plus: self.parse_binary,
			TokenKind.Minus: self.parse_binary,
			TokenKind.Multiply: self.parse_binary,
			TokenKind.Divide: self.parse_binary,
			TokenKind.Mod: self.parse_binary,
			TokenKind.Pow: self.parse_binary,
			TokenKind.Equal: self.parse_binary,
			TokenKind.Diff: self.parse_binary,
			TokenKind.Less: self.parse_binary,
			TokenKind.LessEqual: self.parse_binary,
			TokenKind.Greater: self.parse_binary,
			TokenKind.GreaterEquals: self.parse_binary,
			TokenKind.LogicAnd: self.parse_binary,
			TokenKind.LogicOr: self.parse_binary,
			TokenKind.Assign: self.parse_binary
		}

	def next(self) -> Token|None:
		self.current = self.lexer.lex()
		return self.current

	def parse(self) -> Node|None:
		self.next()
		body = []

		while self.current and self.current.kind not in (TokenKind.CloseBrace, TokenKind.EOI):
			body.append(self.parse_expr())

		return CompoundNode(body)

	def parse_expr(self, precedence: int = 0) -> Node|None:
		token = self.current
		if not token: return

		prefix_parselet = self.prefix_parselets.get(token.kind)
		if not prefix_parselet:
			print(f'Unexpected token {token.kind}', file=sys.stderr)
			exit(1)

		left = prefix_parselet()

		while self.current and precedence < self.PRECEDENCE.get(self.current.kind, 0):
			token = self.current
			infix_parselet = self.infix_parselets.get(token.kind)

			if infix_parselet is None:
				break

			left = infix_parselet(left)

		return left

	def parse_literal(self) -> Node|None:
		token = self.current
		if not token: return
		self.next()
		return LiteralNode(token)

	def parse_prefix(self) -> Node|None:
		token = self.current
		if not token: return
		self.next()
		expr = self.parse_expr(self.PRECEDENCE.get(token.kind, 0))
		if not expr: return
		return UnaryNode(expr, token)

	def parse_group(self) -> Node|None:
		self.next()
		expr = self.parse_expr()
		if self.current != TokenKind.CloseParen:
			print(f'Expected {TokenKind.CloseParen}, not {self.current}', file=sys.stderr)
			exit(1)
		self.next()
		return expr

	def parse_binary(self, left: Node) -> Node|None:
		token = self.current
		if not token: return
		self.next()
		precedence = self.PRECEDENCE.get(token.kind, 0)

		if token.kind == TokenKind.Pow:
			precedence -= 1

		right = self.parse_expr(precedence)
		if not right: return
		return BinaryNode(left, token, right)

	def parse_if(self) -> Node|None:
		self.next()
		cmp = self.parse_expr()
		if not cmp: return

		body = self.parse_compound()
		if not body: return

		else_ = None
		if self.current:
			if self.current.kind == TokenKind.Elsif:
				else_ = self.parse_if()
			elif self.current.kind == TokenKind.Else:
				self.next()
				else_ = self.parse_expr()

		return IfNode(cmp, body, else_)

	def parse_compound(self) -> Node|None:
		self.next()
		body = []

		while self.current and self.current.kind != TokenKind.CloseBrace:
			body.append(self.parse_expr())

		if not self.current or self.current.kind != TokenKind.CloseBrace:
			print(f'Expected {TokenKind.CloseBrace}, not {self.current}', file=sys.stderr)
			exit(1)

		self.next()
		return CompoundNode(body)
