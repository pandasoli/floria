from enum import Enum, auto

# this is for primitives, for compound types you should use a union instead.
class Type(Enum):
	Int = auto()
	Float = auto()
	Char = auto()
	String = auto()
	Bool = auto()
	Void = auto()

