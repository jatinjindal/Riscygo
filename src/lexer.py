#!/usr/bin/env python2

import argparse
import sys

import ply.lex as lex

"""
A Sample Program for lexing

tokens = ('NAME', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS')

t_ignore = ' \t'
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_NAME   = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

lex.lex()

lex.input("x = 32222 * 4 + 5 * 6")
while True:
    tok = lex.token()
    if not tok: break
    print tok
"""

class GoLexer(object):

        # List of token names.   This is always required
     reserved = {
   'break'      :'BREAK'
   'default':'DEFAULT'
   'func':'FUNC'
   'interface':'INTERFACE'
   'select':'SELECT'
   'case':'CASE'
   'defer':'DEFER'
   'go':'GO'
   'map':'MAP'
   'struct':'STRUCT'
   'chan':'CHAN'
   'else':'ELSE'
   'goto':'GOTO'
   'package':'PACKAGE'
   'switch':'SWITCH'
   'const':'CONST'
   'fallthrough':'FALLTHROUGH'
   'if':'IF'
   'range':'RANGE'
   'type':'TYPE'
   'continue':'CONTINUE'
   'for':'FOR'
   'import':'IMPORT'
   'return':'RETURN'
   'var':'VAR'

 }
    tokens = ('LT', 'GT','LE','GE','EQ', 'NE','NOT','LOR','LAND',
      'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'OR', 'XOR', 'LSHIFT', 'RSHIFT', 'AND', 'ANDNOT',
    'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL', 'LSHIFTEQUAL', 'RSHIFTEQUAL', 'ANDEQUAL', 'OREQUAL', 'XOREQUAL', 'AUTOASIGN', 'ANDNOTEQUAL', 
    'ID','LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON',
    'ELLIPSIS',
    
    ) + list(reserved.values())

    # Regular expression rules for operators


    #Relation operators
    t_LT               = r'<'
    t_GT               = r'>'
    t_LE               = r'<='
    t_GE               = r'>='
    t_EQ               = r'=='
    t_NE               = r'!='
    t_NOT              = r'~'
    t_LOR              = r'\|\|'
    t_LAND             = r'&&'

    #Arithmetic operators
    t_PLUS             = r'\+'
    t_MINUS            = r'-'
    t_TIMES            = r'\*'
    t_DIVIDE           = r'/'
    t_MODULO           = r'%'
    t_OR               = r'\|'
    t_XOR              = r'\^'
    t_LSHIFT           = r'<<'
    t_RSHIFT           = r'>>'
    t_AND              = r'&'
    #implemented by them but not needed
    t_ANDNOT           = r'&^'

    #Assignment Operators
    t_EQUALS           = r'='
    t_TIMESEQUAL       = r'\*='
    t_DIVEQUAL         = r'/='
    t_MODEQUAL         = r'%='
    t_PLUSEQUAL        = r'\+='
    t_MINUSEQUAL       = r'-='
    t_LSHIFTEQUAL      = r'<<='
    t_RSHIFTEQUAL      = r'>>='
    t_ANDEQUAL         = r'&='
    t_OREQUAL          = r'\|='
    t_XOREQUAL         = r'\^='
    t_AUTOASIGN        = r':='

    t_ANDNOTEQUAL           = r'&^='

    t_LPAREN           = r'\('
    t_RPAREN           = r'\)'
    t_LBRACKET         = r'\['
    t_RBRACKET         = r'\]'
    t_LBRACE           = r'\{'
    t_RBRACE           = r'\}'
    t_COMMA            = r','
    t_PERIOD           = r'\.'
    t_SEMI             = r';'
    t_ELLIPSIS         = r'\.\.\.'


    def t_ID(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value,'ID')    # Check for reserved words
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print ("Illegal character '%s'" % str(t.value[0]))
        print ("Value of the illegal token is '%s'" % str(t.value))
        sys.exit(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module = self, **kwargs)

    def lex(self, raw_data):
        self.lexer.input(raw_data)
        while True:
            tok = self.lexer.token()
            if not tok: break
            print (tok)

def main():
    parser = argparse.ArgumentParser(description = 'A Lexer for Golang')
    parser.add_argument('--cfg', required = True, help = 'color configuration file')
    parser.add_argument('input', help = 'input Golang file')
    parser.add_argument('--out', required = True, help = 'HTML output file')
    args = parser.parse_args()
    with open(args.input, 'r') as f:
        raw_data = ''.join(f.readlines())
    lexer = GoLexer()
    lexer.build()
    lexer.lex(raw_data)

if __name__ == '__main__':
    main()
