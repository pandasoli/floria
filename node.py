from dataclasses import dataclass
from typing import Union
from token_ import Token

Node = Union[
	# Literal
	'LiteralNode',

	# Compound
	'CompoundNode',

	# Operations
	'BinaryNode', 'UnaryNode',

	# Comparison
	'IfNode'
]

@dataclass
class LiteralNode:
	token: Token

	def __repr__(self):
		return f'{self.token}'

@dataclass
class BinaryNode:
	left: Node
	op: Token
	right: Node

	def __repr__(self):
		return f'({self.left} {self.op} {self.right})'

@dataclass
class UnaryNode:
	expr: Node
	op: Token

	def __repr__(self):
		return f'({self.op}{self.expr})'

@dataclass
class IfNode:
	cmp: Node
	body: Node
	else_: Node|None

	def __repr__(self):
		else_ = f' else {{ {self.else_} }}' if self.else_ else ''
		return f'if {self.cmp} {self.body}{else_}'

@dataclass
class CompoundNode:
	body: list[Node]

	def __repr__(self):
		exprs = [expr.__repr__() for expr in self.body]
		return f"{{ {' '.join(exprs)} }}"
