from node import BinaryNode, CompoundNode, IfNode, LiteralNode, Node, UnaryNode
from types_ import Type
from token_ import TokenKind

def check_type(ast: Node|None) -> Type|None:
	match ast:
		case LiteralNode():
			match ast.token.kind:
				case TokenKind.Ident:
					print("Error - cannot trace variables yet")
					return None

				case TokenKind.Integer:
					return Type.Int

				case TokenKind.Float:
					return Type.Float

				case TokenKind.Char:
					return Type.Char

				case TokenKind.String:
					return Type.String

				case TokenKind.True_ | TokenKind.False_:
					return Type.Bool

		case CompoundNode():
			# return the type of the last expression
			if len(ast.body) > 0:
				return check_type(ast.body[len(ast.body) - 1])

			return Type.Void

		case BinaryNode():
			# both types need to be compatible
			left_type = check_type(ast.left)
			right_type = check_type(ast.right)

			if not left_type or not right_type:
				print(f"Error - Invalid types '{left_type}' and '{right_type}'.")
				return None

			if not is_type_compatible(left_type, right_type):
				print("Error - types in binary node are not compatible.")
				print(f"Left: {left_type}")
				print(f"Right: {right_type}")
				return None
			
			
			# check if the operation is supported by the types
			# +             | Int, Float, String
			# -, *, /, ^, % | Int, Float
			# >, >=, <, <=  | Int, Float
			# ==, !=        | any, but they need to be compatible
			# and, or       | Bool

			supported = []
			match ast.op.kind:
				case TokenKind.Plus:
					supported = [Type.Int, Type.Float, Type.String]
				
				case TokenKind.Minus | TokenKind.Multiply | TokenKind.Divide | TokenKind.Pow | TokenKind.Mod | TokenKind.Less | TokenKind.LessEqual | TokenKind.Greater | TokenKind.GreaterEquals:
					supported = [Type.Int, Type.Float]

				case TokenKind.Equal | TokenKind.Diff:
					# skip the verification
					return merge_types(left_type, right_type)

				case TokenKind.LogicAnd | TokenKind.LogicOr:
					supported = [Type.Bool]

				case _:
					print(f"Panic - Unexpected type: {ast.op}")
					return None

			if not (left_type in supported and right_type in supported):
				print(f"Error - Types '{left_type}' and '{right_type}' aren't supported by the operator '{ast.op.literal}'.")
				return None

			# types are compatible with each other and with the operator, return the merged one.
			# this rule can be changed based on the operator as well (like, a division always returns Float)
			return merge_types(left_type, right_type)

		case UnaryNode():
			operand_type = check_type(ast.expr)
			
			if not operand_type:
				print(f"Error - Invalid type '{operand_type}'.")
				return None

			# operators are '+' and '-', so Int and Float are supported.
			supported = [Type.Int, Type.Float]
			
			if operand_type not in supported:
				print(f"Error - Type '{operand_type}' isn't supported by the operator '{ast.op.literal}'.")
				return None

			return operand_type

		case IfNode():
			# check if compare expression is boolean
			cmp_type = check_type(ast.cmp)
			if cmp_type != Type.Bool:
				print(f"Error - Compare expression must be boolean, got '{cmp_type}'.")
				return None

			# no else - void
			# body and else equal - their type
			# body and else not equal - error

			if ast.else_ == None:
				return Type.Void
			
			body_type = check_type(ast.body)
			else_type = check_type(ast.else_)
			
			if body_type == else_type:
				return body_type
			else:
				print("Error - 'if' and 'else' clauses have different types.")
				print(f"'if': {body_type}")
				print(f"'else': {else_type}")

				return None

		case None:
			return None

# returns whether the type is compatible with each other (e.g.: Int with Float)
def is_type_compatible(a: Type, b: Type) -> bool:
	return merge_types(a, b) != None

# returns the merged type, which is the type out of the two that can represent both.
# ex.: (Int, Float) -> Float, because every Int value can be represented by a Float.
def merge_types(a: Type, b: Type) -> Type|None:
	# equal types return themselves
	if a == b:
		return a
	
	# pairs of supported types and the merged one
	types: list[tuple[list[Type], Type]] = [
		([Type.Int, Type.Float], Type.Float),
	]
	
	for type_list, corresponding in types:
		if a in type_list or b in type_list:
			return corresponding
	
	# types cannot be merged
	return None
