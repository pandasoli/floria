import sys
from token_ import TokenKind
from types_ import Type
from node import Node, BinaryNode, CompoundNode, IfNode, LiteralNode, UnaryNode
from typednode import TypedBinaryNode, TypedIfNode, TypedNode, TypedCompundNode, TypedLiteralNode, TypedUnaryNode

def merge_types(a: Type, b: Type) -> Type|None:
	if a == b: return a

	types: list[tuple[list[Type], Type]] = [
		([Type.Int, Type.Float], Type.Float)
	]

	for list_, match_ in types:
		if a in list_ and b in list_:
			return match_

	return None

class TypeChecker:
	def check(self, node: Node) -> TypedNode|None:
		match node:
			case LiteralNode(): return self.literal(node)
			case CompoundNode(): return self.compound(node)
			case BinaryNode(): return self.binary(node)
			case UnaryNode(): return self.unary(node)
			case IfNode(): return self.if_(node)

	def if_(self, node: IfNode) -> TypedIfNode|None:
		cmp = self.check(node.cmp)
		if not cmp: return

		if cmp.type != Type.Bool:
			print(f'Expected if comparision to be of boolean type')
			return

		body = self.check(node.body)
		if not body: return

		if not node.else_:
			return TypedIfNode(cmp, body, None, Type.Void)

		else_ = self.check(node.else_)
		if not else_: return

		if body.type != else_.type:
			print(f'Invalid if with two different return types')
			return

		return TypedIfNode(cmp, body, else_, body.type)

	def unary(self, node: UnaryNode) -> TypedUnaryNode|None:
		expr = self.check(node.expr)
		if not expr: return

		supported = [Type.Int, Type.Float]

		if expr.type not in supported:
			print(f'Incompatible operation for type {expr.type}', file=sys.stderr)
			return

		return TypedUnaryNode(expr, node.op, expr.type)

	def binary(self, node: BinaryNode) -> TypedBinaryNode|None:
		left = self.check(node.left)
		if not left: return
		right = self.check(node.right)
		if not right: return

		supported = []
		match node.op.kind:
			case TokenKind.Plus | TokenKind.Multiply:
				supported = [Type.Int, Type.Float, Type.String]
			case TokenKind.Minus | TokenKind.Divide | TokenKind.Pow | TokenKind.Mod | TokenKind.Less | TokenKind.LessEqual | TokenKind.Greater | TokenKind.GreaterEquals:
				supported = [Type.Int, Type.Float]
			case TokenKind.LogicAnd | TokenKind.LogicOr:
				supported = [Type.Bool]

			case TokenKind.Equal | TokenKind.Diff:
				compatible = merge_types(left.type, right.type) != None
				if compatible:
					return TypedBinaryNode(left, right, node.op, Type.Bool)

			case _:
				raise Exception(f'Unexpected operator {node.op}')

		if left.type not in supported or right.type not in supported:
			print(f'Incompatible operation between types {left.type} and {right.type}', file=sys.stderr)
			return

		return TypedBinaryNode(left, right, node.op, Type.Int)

	def compound(self, node: CompoundNode) -> TypedCompundNode:
		body = [x for x in map(self.check, node.body) if x is not None]

		return TypedCompundNode(
			body,
			body[-1].type if len(body) > 0 else Type.Void
		)

	def literal(self, node: LiteralNode) -> TypedLiteralNode|None:
		match node.token.kind:
			case TokenKind.Ident:
				raise Exception('Error - cannot trace variables yet')

			case TokenKind.Integer: return TypedLiteralNode(node.token, Type.Int)
			case TokenKind.Float: return TypedLiteralNode(node.token, Type.Float)
			case TokenKind.Char: return TypedLiteralNode(node.token, Type.Char)
			case TokenKind.String: return TypedLiteralNode(node.token, Type.String)
			case TokenKind.True_ | TokenKind.False_: return TypedLiteralNode(node.token, Type.Bool)
