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
    tokens = (
        'FOO',
        'BAR'
    )

    t_FOO = r'FOO'
    t_BAR = r'BAR'

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
