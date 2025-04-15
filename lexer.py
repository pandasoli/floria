import sys
from token_ import Token, TokenKind, Keywords

class Lexer:
	text: str
	pos: int
	current: str

	def __init__(self, text: str):
		self.text = text
		self.pos = 0
		self.current = text[0]

	def next(self) -> str:
		self.pos += 1
		self.current = self.text[self.pos]
		return self.current

	def lex(self) -> Token|None:
		while self.current in (' ', '\t', '\r', '\n'):
			self.next()

		kind = TokenKind.Unknown
		start = self.pos

		match self.current:
			case '\0': kind = TokenKind.EOI

			case '+': kind = TokenKind.Plus; self.next()
			case '-': kind = TokenKind.Minus; self.next()
			case '*': kind = TokenKind.Multiply; self.next()
			case '/': kind = TokenKind.Divide; self.next()
			case '%': kind = TokenKind.Mod; self.next()
			case '^': kind = TokenKind.Pow; self.next()

			case '(': kind = TokenKind.OpenParen; self.next()
			case ')': kind = TokenKind.CloseParen; self.next()
			case '{': kind = TokenKind.OpenBrace; self.next()
			case '}': kind = TokenKind.CloseBrace; self.next()
			case ',': kind = TokenKind.Comma; self.next()

			case '=':
				kind = TokenKind.Assign; self.next()

				if   self.current == '=': kind = TokenKind.Equal; self.next()
				elif self.current == '<': kind = TokenKind.LessEqual; self.next()
				elif self.current == '>': kind = TokenKind.GreaterEquals; self.next()

			case '<':
				kind = TokenKind.Less; self.next()
				if self.current == '=': kind = TokenKind.LessEqual; self.next()

			case '>':
				kind = TokenKind.Greater; self.next()
				if self.current == '=': kind = TokenKind.GreaterEquals; self.next()

			case '!':
				if self.next() == '=': kind = TokenKind.Diff; self.next()
				else: self.pos -= 1

			case '\'':
				kind = TokenKind.Char

				while self.next() != '\'': ...
				self.next()

				if self.pos - start > 3:
					kind = TokenKind.String

			case self.current if self.current.isdigit():
				kind = TokenKind.Integer
				while self.current.isdigit(): self.next()

				if self.current == '.':
					kind = TokenKind.Float
					self.next()
					while self.current.isdigit(): self.next()

			case self.current if self.current.isalpha():
				kind = TokenKind.Ident
				while self.current.isalpha() or self.current.isdigit(): self.next()

				for type, kw in Keywords:
					if self.text[start:self.pos] == kw:
						kind = type
						break

		if kind == TokenKind.Unknown:
			print(f'Found unkonwn token at position {self.pos}', file=sys.stderr)
			return

		return Token(kind, self.text[start:self.pos], start)
