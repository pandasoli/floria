from lexer import Lexer
from token_ import TokenKind
from parser import Parser

def colorfy(text: str):
	l = Lexer(text)
	tokens = []

	while True:
		t = l.lex()
		if not t: break

		tokens.append(t)

		if t.kind == TokenKind.EOI:
			break

	indent = 0

	for t in tokens:
		match t.kind:
			case TokenKind.If: print('\x1b[38;2;204;153;255mif\x1b[m ', end='')
			case TokenKind.Elsif: print('\x1b[38;2;204;153;255melsif\x1b[m ', end='')
			case TokenKind.Else: print('\x1b[38;2;204;153;255melse\x1b[m ', end='')

			case TokenKind.Integer | TokenKind.Float: print(f'\x1b[38;2;221;160;221m{t.literal}\x1b[m ', end='')
			case TokenKind.String | TokenKind.Char: print(f'\x1b[94m{t.literal}\x1b[m ', end='')

			case TokenKind.Plus | TokenKind.Minus | TokenKind.Multiply | TokenKind.Divide | TokenKind.Mod | TokenKind.Pow:
				print(f'\x1b[92m{t.literal}\x1b[m ', end='')

			case TokenKind.Equal: print('\x1b[95m==\x1b[m ', end='')
			case TokenKind.Less: print('\x1b[95m<\x1b[m ', end='')
			case TokenKind.LessEqual: print('\x1b[95m<=\x1b[m ', end='')
			case TokenKind.Greater: print('\x1b[95m>\x1b[m ', end='')
			case TokenKind.GreaterEquals: print('\x1b[95m=>\x1b[m ', end='')

			case TokenKind.OpenBrace:
				indent += 2
				print('\x1b[90m{\x1b[m\n' + indent * ' ', end='')
			case TokenKind.CloseBrace:
				indent -= 2
				print('\n' + indent * ' ' + '\x1b[90m}\x1b[m')

			case _: print(indent * ' ', t, ' ', end='', sep='')

def main():
	# colorfy("if h1 == 12 { 'Hello!' * 2 } elsif a == 6 {} elsif b == 2 {} else {}\0")
	l = Lexer("if h1 == 12 { echo 'Hello!' } elsif a == 6 {} elif b == 2 {}\0")
	p = Parser(l)
	n = p.parse()

	print(n)

if __name__ == '__main__':
	main()
