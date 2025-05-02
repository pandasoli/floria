from dataclasses import dataclass
from typing import Union
from token_ import Token
from node import LiteralNode
from types_ import Type

TypedNode = Union[
	# Literal
	'TypedLiteralNode',

	# Compound
	'TypedCompundNode',

	# Operations
	'TypedBinaryNode', 'TypedUnaryNode',

	# Comparison
	'TypedIfNode'
]

@dataclass
class TypedLiteralNode(LiteralNode):
	type: Type

	def __repr__(self):
		return f'({self.type}) {self.token}'

@dataclass
class TypedBinaryNode:
	left: TypedNode
	right: TypedNode
	op: Token
	type: Type

	def __repr__(self):
		return f'{self.type}({self.left} {self.op} {self.right})'

@dataclass
class TypedUnaryNode:
	expr: TypedNode
	op: Token
	type: Type

	def __repr__(self):
		return f'{self.type}({self.op}{self.expr})'

@dataclass
class TypedIfNode:
	cmp: TypedNode
	body: TypedNode
	else_: TypedNode|None
	type: Type

	def __repr__(self):
		else_ = f' else {{ {self.else_} }}' if self.else_ else ''
		return f'{self.type}(if {self.cmp} {self.body}{else_})'

@dataclass
class TypedCompundNode:
	body: list[TypedNode]
	type: Type

	def __repr__(self):
		exprs = [expr.__repr__() for expr in self.body]
		return f"{self.type}({{ {' '.join(exprs)} }})"
