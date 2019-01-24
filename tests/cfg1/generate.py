import sys
import random as rand

val=sys.argv[1]
filename=str(val)+".cfg"
f=open(filename,'w+')

reserved = {
        'break': 'BREAK',
        'default': 'DEFAULT',
        'func': 'FUNC',
        'interface': 'INTERFACE',
        'select': 'SELECT',
        'case': 'CASE',
        'defer': 'DEFER',
        'go': 'GO',
        'map': 'MAP',
        'struct': 'STRUCT',
        'chan': 'CHAN',
        'else': 'ELSE',
        'goto': 'GOTO',
        'package': 'PACKAGE',
        'switch': 'SWITCH',
        'const': 'CONST',
        'fallthrough': 'FALLTHROUGH',
        'if': 'IF',
        'range': 'RANGE',
        'type': 'TYPE',
        'continue': 'CONTINUE',
        'for': 'FOR',
        'import': 'IMPORT',
        'return': 'RETURN',
        'var': 'VAR',
    }

types = {
    'bool': 'BOOL',
    'byte': 'BYTE',
    'int': 'INT',
    'uint8': 'UINT8',
    'uint16': 'UINT16',
    'uint32': 'UINT32',
    'uint64': 'UINT64',
    'int8': 'INT8',
    'int16': 'INT16',
    'int32': 'INT32',
    'int64': 'INT64',
    'int': 'INT',
    'uint': 'UINT',
    'float32': 'FLOAT32',
    'float64': 'FLOAT64',
    'uintptr': 'UINTPTR',
    'string': 'STRING',
    'error': 'ERROR',
}

constants = {
    'true': 'TRUE',
    'false': 'FALSE',
    'iota': 'IOTA',
    'nil': 'NIL',
}

combined_map = dict(reserved, **dict(types, **constants))

tokens = [
    'LT', 'GT', 'LE', 'GE', 'EQ', 'NE', 'NOT', 'LNOT', 'LOR', 'LAND',
    'LARROW', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'OR', 'XOR',
    'LSHIFT', 'RSHIFT', 'AND', 'ANDNOT', 'INCR', 'DECR', 'EQUALS',
    'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
    'LSHIFTEQUAL', 'RSHIFTEQUAL', 'ANDEQUAL', 'OREQUAL', 'XOREQUAL',
    'AUTOASIGN', 'ANDNOTEQUAL', 'ID', 'LPAREN', 'RPAREN', 'LBRACKET',
    'RBRACKET', 'LBRACE', 'RBRACE', 'COMMA', 'PERIOD', 'SEMI', 'COLON',
    'ELLIPSIS', 'CHARACTER', 'COMMENT', 'MULTICOMMENT', 'INTEGER', 'FLOAT','STRINGVAL','NUMBER'
] + list(set(combined_map.values()))

for x in tokens:
	r = rand.randint(100, 255)
	b = rand.randint(100, 255)
	g = rand.randint(100, 255)
	r, b, g = list(map(lambda x: hex(x)[2:], [r, g, b]))
	color = '0x' + r + b + g
	f.write(x+" "+str(color)+"\n")