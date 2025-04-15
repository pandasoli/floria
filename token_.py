from dataclasses import dataclass
from enum import Enum, auto

class TokenKind(Enum):
	Unknown = 0

	EOI = auto()

	# Literals
	Ident = auto()
	Integer = auto()
	Float = auto()
	String = auto()
	Char = auto()

	# Arithimatic Operators
	Plus = auto()
	Minus = auto()
	Multiply = auto()
	Divide = auto()
	Mod = auto()
	Pow = auto()

	# Comparision Operators
	Equal, Diff = auto(), auto()
	Less, LessEqual = auto(), auto()
	Greater, GreaterEquals = auto(), auto()

	# Delimiters
	OpenParen, CloseParen = auto(), auto()
	OpenBrace, CloseBrace = auto(), auto()
	Comma = auto()

	Assign = auto()

	# Logical Operators
	LogicAnd, LogicOr = auto(), auto()

	# Statements
	If, Elsif, Else = auto(), auto(), auto()

Keywords = (
	# Logical Operators
	(TokenKind.LogicAnd, 'and'),
	(TokenKind.LogicOr, 'or'),

	# Statements
	(TokenKind.If, 'if'),
	(TokenKind.Elsif, 'elsif'),
	(TokenKind.Else, 'else')
)

@dataclass
class Token:
	kind: TokenKind
	literal: str
	start: int

	def __repr__(self):
		return self.literal
