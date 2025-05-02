from enum import Enum, auto

# This is for primitives, for compound types use a union instead.
class Type(Enum):
	Int = auto()
	Float = auto()
	Char = auto()
	String = auto()
	Bool = auto()
	Void = auto()
