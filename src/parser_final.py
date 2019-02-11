#!/usr/bin/env python2



# CHANGES MADE
# 1) removed epsilon from SimpleStmt
# 2) added special symbol before IdentifierList
# 3) Removed Types from CompositeLit (Go Specs WRONG)


import argparse
import re
import sys
from sys import argv

import ply.lex as lex

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
    'ELLIPSIS', 'CHARACTER', 'COMMENT', 'MULTICOMMENT', 'INTEGER', 'FLOAT',
    'STRINGVAL','newline','SPECIAL'
] + list(set(combined_map.values()))

# Regular expression rules for operators

# Relation operators
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_NOT = r'~'
t_LNOT = r'!'
t_LOR = r'\|\|'
t_LAND = r'&&'
t_LARROW = r'<\-'
t_SPECIAL= r'\?'

# Arithmetic operators
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_OR = r'\|'
t_XOR = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_AND = r'&'
t_ANDNOT = r'&\^'
t_INCR = r'\+\+'
t_DECR = r'\-\-'

# Assignment operators
t_EQUALS = r'='
t_AUTOASIGN = r':='
t_TIMESEQUAL = r'\*='
t_DIVEQUAL = r'/='
t_MODEQUAL = r'%='
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'\-='
t_LSHIFTEQUAL = r'<<='
t_RSHIFTEQUAL = r'>>='
t_ANDEQUAL = r'&='
t_OREQUAL = r'\|='
t_XOREQUAL = r'\^='
t_ANDNOTEQUAL = r'&\^='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r'\,'
t_PERIOD = r'\.'
t_SEMI = r';'
t_COLON = r':'
t_ELLIPSIS = r'\.\.\.'

t_STRINGVAL = r'\"([^\\\n]|(\\.))*?\"'
t_CHARACTER = r'(L)?\'([^\\\n]|(\\.))*?\''

t_ignore = ' \t'

def t_FLOAT( t):
    r'(\d+\.\d*(e|E)[\+|\-]?\d+)|((\d+)(e|E)[\+|\-]?\d+)|(\.\d+(e|E)[\+|\-]?\d+)|(\d+\.\d*)|(\.\d+)'
    t.value=float(t.value)
    return t

def t_INTEGER( t):
    r'0[xX][0-9a-fA-F]+|\d+'
    t.value=int(t.value)
    return t

def t_ID( t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = combined_map.get(t.value, 'ID')
    return t

def t_MULTICOMMENT( t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_COMMENT( t):
    r'//.*\n'
    t.lexer.lineno += 1
    return t

def t_newline( t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_error( t):
    print("Illegal character '%s'" % str(t.value[0]))
    print("Value of the illegal token is '%s'" % str(t.value))
    t.lexer.skip(1)


lexer = lex.lex()



# Give the lexer some input
# data = raw_input('calc > ') 
# lexer.input(data)
 
# # Tokenize
# while True:
#     tok = lexer.token()
#     if not tok: 
#         break      # No more input
#     print(tok)

# while 1:
#     try:
#         s = raw_input('calc > ')
#     except EOFError:
#         break
#     if not s:
#         continue
#     lexer.input(s)
#     tok = lexer.token()
#     print tok
    # yacc.parse(s, tracking = True)



class Node:
     def __init__(self,type,children=None,leaf=None):
          self.type = type
          if children:
               self.children = children
          else:
               self.children = [ ]
          self.leaf = leaf

# def p_empty(p):
#      'empty :'
#      pass

#-------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------


# Statement = Declaration | LabeledStmt | SimpleStmt |
#             GoStmt | ReturnStmt | BreakStmt | ContinueStmt | GotoStmt |
#             FallthroughStmt | Block | IfStmt | SwitchStmt | SelectStmt | ForStmt |
#             DeferStmt .

def p_Start(p):
  '''Start : SourceFile'''
  print "Succesfully completed"


def p_SourceFile(p):
  '''SourceFile : PackageClause terminator Repeatnewline RepeatTopLevelDecl
          | PackageClause Repeatnewline RepeatTopLevelDecl
          | PackageClause terminator RepeatTopLevelDecl
  '''
  #print "here Sourcefile"


def p_PackageClause(p):
  'PackageClause : PACKAGE PackageName '


def p_PackageName(p):
  'PackageName : ID '

def p_RepeatTopLevelDecl(p):
  '''RepeatTopLevelDecl : TopLevelDecl RepeatTopLevelDecl
                      | empty'''

def p_TopLevelDecl(p):
  '''TopLevelDecl : Declaration Repeat_multi_newline
                  | FunctionDecl Repeat_multi_newline'''


def p_StatementList(p):
    '''StatementList : Statement RepeatTerminator  StatementList
                      | Statement Repeatnewline  StatementList
                     | Statement
                     | Statement RepeatTerminator Repeatnewline StatementList
                     | empty 
       '''

# def p_StatementList(p):
#     '''StatementList : Statement RepeatTerminator  StatementList
#              | Repeatnewline StatementList
#                      | Statement
#                      | empty 
#        '''


#Add Declaration
def p_Statement(p):
    ''' Statement : Declaration
                 | LabeledStmt  
                 | SimpleStmt
                 | ReturnStmt   
                 | BreakStmt
                 | ContinueStmt
                 | GotoStmt
                 | Block
                 | IfStmt
                 | SwitchStmt  
                 | ForStmt     
                 | DeferStmt   
    '''

# Declaration   = ConstDecl | TypeDecl | VarDecl .
# I am also adding FunctionDecl also part of it, though is actually part of Top Level Decl
def p_Declaration(p):
    ''' Declaration : ConstDecl 
                    | TypeDecl
                    | VarDecl  '''

# ConstDecl = "const" ( ConstSpec | "(" { ConstSpec ";" } ")" ) .
def p_ConstDecl(p):
    ''' ConstDecl : CONST ConstSpec'''


# ConstSpec      = IdentifierList [ [ Type ] "=" ExpressionList ] .
##Again Identifier Problem but becuase of const no problem
def p_ConstSpec(p):
    ''' ConstSpec : IdentifierList
                  | IdentifierList EQUALS ExpressionList'''





# TypeDecl = "type" ( TypeSpec | "(" { TypeSpec ";" } ")" ) .
def p_TypeDecl(p):
    ''' TypeDecl : TYPE Repeat_multi_newline TypeSpec '''

# TypeSpec = AliasDecl | TypeDef 
def p_TypeSpec(p):
    ''' TypeSpec : TypeDef '''

# TypeDef = identifier Type .
def p_TypeDef(p):
    ''' TypeDef : ID Types '''






#  VarDecl     = "var" ( VarSpec | "(" { VarSpec ";" } ")" ) .
#  VarSpec = IdentifierList ( Type [ "=" ExpressionList ] | "=" ExpressionList ) 
def p_VarDecl(p):
    ''' VarDecl : VAR Repeat_multi_newline VarSpec '''

#Didnt understand why did he add empty also in VarSpec
def p_VarSpec(p):
    ''' VarSpec : IdentifierList Types
                | IdentifierList Types EQUALS Repeat_multi_newline ExpressionList 
                | IdentifierList EQUALS Repeat_multi_newline ExpressionList '''


# FunctionDecl = "func" FunctionName Signature [ FunctionBody ] .
# FunctionName = identifier .
# FunctionBody = Block .
def p_FunctionDecl(p):
    ''' FunctionDecl : FunctionMarker  FunctionBody
                      | FunctionMarker '''

def p_FunctionMarker(p):
    ''' FunctionMarker : FUNC Repeat_multi_newline FunctionName Signature '''


def p_FunctionName(p):
    ''' FunctionName : ID '''
#Didn't include variadic functions, it is defined by ... below

#  Signature      = Parameters [ Result ] .
#  Result         = Parameters | Type .
#  Parameters     = "(" [ ParameterList [ "," ] ] ")" .
#  ParameterList  = ParameterDecl { "," ParameterDecl } .
#  ParameterDecl = [ IdentifierList ] [ "..." ] Type .

def p_Signature(p):
    ''' Signature : Parameters 
                  | Parameters Result '''


# Parameters can't end in ,
def p_Parameters(p):
    ''' Parameters : LPAREN Repeat_multi_newline RPAREN
                   | LPAREN Repeat_multi_newline ParameterList RPAREN '''


def p_ParameterList(p):
    ''' ParameterList : ParameterDecl RepeatParameterDecl '''

def p_RepeatParameterDecl(p):
    ''' RepeatParameterDecl : COMMA Repeat_multi_newline ParameterDecl RepeatParameterDecl
                            | empty '''

def p_ParameterDecl(p):
    ''' ParameterDecl : ID Types
                      | Types '''


def p_Result(p):
    ''' Result : Parameters
               | Types '''




def p_FunctionBody(p):
    ''' FunctionBody : Block '''



 # LabeledStmt = Label ":" Statement .
 # Label       = identifier .

def p_terminator(p):
    "terminator : SEMI"

def p_RepeatTerminator(p):
    '''RepeatTerminator :  RepeatTerminator Repeat_multi_newline terminator 
                        |  terminator
    '''
def p_Repeatnewline(p):
  '''Repeatnewline : newline Repeatnewline
        | newline'''

#doubt
def p_Repeat_multi_newline(p):
  '''Repeat_multi_newline : newline Repeat_multi_newline
        | empty'''


def p_LabeledStmt(p):
    '''LabeledStmt : Label COLON Repeat_multi_newline Statement'''


def p_Label(p):
    '''Label : ID'''



# SimpleStmt = EmptyStmt | ExpressionStmt | SendStmt | IncDecStmt | Assignment | ShortVarDecl .
# EmptyStmt = .
# ExpressionStmt = Expression .
# IncDecStmt = Expression ( "++" | "--" ) .
# Assignment = ExpressionList assign_op ExpressionList .
# assign_op = [ add_op | mul_op ] "=" .
# ShortVarDecl = IdentifierList ":=" ExpressionList .


# EMPTY STATEMENT REMOVED FROM SIMPLESTATEMENT
def p_SimpleStmt(p):
    '''SimpleStmt : Assignment
        | ShortVarDecl
        | IncDecStmt
        | ExpressionStmt'''

# def p_emptyStmt(p):
#     '''EmptyStmt : empty'''

def p_ExpressionStmt(p):
    '''ExpressionStmt : Expression'''

def p_IncDecStmt(p):
    '''IncDecStmt : Expression INCR 
        | Expression DECR  '''

# I am self defining this assignment operator due to lack in our grammar
def p_AssignOp(p):
    '''AssignOp : TIMESEQUAL
            | DIVEQUAL 
            | MODEQUAL 
            | PLUSEQUAL 
            | MINUSEQUAL
            | LSHIFTEQUAL 
            | RSHIFTEQUAL 
            | ANDEQUAL 
            | OREQUAL 
            | XOREQUAL 
            | ANDNOTEQUAL 
    '''

#I am currently following official go language and not including IdentifierList=ExpressionList
def p_Assignments(p):
    '''Assignment : ExpressionList AssignOp  Repeat_multi_newline ExpressionList
                | ExpressionList  EQUALS  Repeat_multi_newline ExpressionList'''

def p_ShortVarDecl(p):
    '''ShortVarDecl : ExpressionList AUTOASIGN Repeat_multi_newline ExpressionList'''

def p_ReturnStmt(p):
    '''ReturnStmt : RETURN
                | RETURN ExpressionList'''

def p_BreakStmt(p):
    '''BreakStmt : BREAK 
                | BREAK Label'''

# Check for conflicts here between continueStmt and BreakStmt
def p_ContinueStmt(p):
    '''ContinueStmt : CONTINUE
                    | CONTINUE Label'''

def p_GotoStmt(p):
    '''GotoStmt : GOTO Label'''

def p_Block(p):
    '''Block : LBRACE Marker StatementList RBRACE
        | LBRACE Repeatnewline Marker StatementList RBRACE'''

def p_Marker(p):
    '''Marker : empty'''

def p_IfStmt(p):
    '''IfStmt : IF Repeat_multi_newline Expression Block
            | IF Repeat_multi_newline Expression Block ELSE Block
            | IF Repeat_multi_newline Expression Block ELSE IfStmt
            | IF Repeat_multi_newline SimpleStmt terminator Expression Block
            | IF Repeat_multi_newline SimpleStmt terminator Expression Block ELSE IfStmt
            | IF Repeat_multi_newline SimpleStmt terminator Expression Block ELSE Block'''

def p_SwitchStmt(p):
    '''SwitchStmt : ExprSwitchStmt'''

# I have followed Go Specs and made Expression optional
def p_ExprSwitchStmt(p):
    '''ExprSwitchStmt : SWITCH Repeat_multi_newline LBRACE Repeat_multi_newline RepeatExprCaseClause RBRACE
                    | SWITCH Repeat_multi_newline Expression LBRACE Repeat_multi_newline RepeatExprCaseClause RBRACE'''

def p_RepeatExprCaseClause(p):
    '''RepeatExprCaseClause : ExprCaseClause RepeatExprCaseClause
                            | empty'''
def p_ExprCaseClause(p):
    '''ExprCaseClause : ExprSwitchCase COLON Repeat_multi_newline StatementList'''

def p_ExprSwitchCase(p):
    '''ExprSwitchCase : CASE Repeat_multi_newline Expression
                    | DEFAULT  Repeat_multi_newline''' 

def p_ForStmt(p):
    '''ForStmt : FOR Repeat_multi_newline Block
            | FOR Repeat_multi_newline Condition Block
            | FOR Repeat_multi_newline ForClause Block'''

def p_ForClause(p):
    '''ForClause : terminator terminator
                | InitStmt terminator terminator
                | terminator Condition terminator
                | terminator terminator PostStmt
                | InitStmt terminator Condition terminator
                | InitStmt terminator terminator PostStmt
                | terminator Condition terminator PostStmt
                | InitStmt terminator Condition terminator PostStmt'''

def p_InitStmt(p):
    'InitStmt : SimpleStmt'

def p_PostStmt(p):
    'PostStmt : SimpleStmt'

def p_Condition(p):
    'Condition : Expression'



def p_DeferStmt(p):
    '''DeferStmt : DEFER PrimaryExpr Arguments'''

#-----------------------------------------------------------

def p_ExpressionList(p):
    ''' ExpressionList : Expression
                       | Expression COMMA Repeat_multi_newline ExpressionList '''

def p_Expression(p):
    '''Expression : Expression LOR Repeat_multi_newline Term1
                  | Term1 '''
    
def p_Term1(p):
    '''Term1 : Term1 LAND Repeat_multi_newline Term2
             | Term2 '''


def p_Term2(p):
    '''Term2 : Term2 Relop Repeat_multi_newline Term3
             | Term3 '''

def p_Relop(p):
    ''' Relop : LT 
              | GT 
              | LE 
              | GE 
              | EQ 
              | NE '''


#Gives the Plus and Minus the same precedence, check it
def p_Term3(p):
    '''Term3 : Term3 PLUS Repeat_multi_newline Term4
             | Term3 MINUS Repeat_multi_newline Term4
             | Term3 OR Repeat_multi_newline Term4
             | Term3 XOR Repeat_multi_newline Term4
             | Term4 '''

#Similary for *, /
def p_Term4(p):
    '''Term4 : Term4 TIMES Repeat_multi_newline Term5
             | Term4 DIVIDE Repeat_multi_newline Term5
             | Term4 MODULO Repeat_multi_newline Term5
             | Term4 LSHIFT Repeat_multi_newline Term5
             | Term4 RSHIFT Repeat_multi_newline Term5
             | Term4 AND Repeat_multi_newline Term5
             | Term4 ANDNOT Repeat_multi_newline Term5
             | Term5 '''


def p_Term5(p):
    '''Term5 : LPAREN Repeat_multi_newline Expression RPAREN
             | UnaryExp '''


def p_UnaryExp(p):
    '''UnaryExp : PrimaryExpr
                | UnaryOp Repeat_multi_newline UnaryExp '''

def p_UnaryOp(p):
    '''UnaryOp : PLUS 
               | MINUS 
               | LNOT 
               | TIMES 
               | AND'''


# // PrimaryExpr =
# //  Operand |
# //  Conversion |
# //  MethodExpr |
# //  PrimaryExpr Selector |
# //  PrimaryExpr Index |
# //  PrimaryExpr Slice |
# //  PrimaryExpr TypeAssertion |
# //PrimaryExpr Arguments .

def p_PrimaryExpr(p):
    '''PrimaryExpr : Operand
                   | PrimaryExpr Selector
                   | PrimaryExpr Index 
                   | PrimaryExpr Arguments '''

# Operand = Literal | OperandName | "(" Expression ")" .
def p_Operand(p):
    ''' Operand : Literal 
                | OperandName '''


#Literal = BasicLit | CompositeLit | FunctionLit .
def p_Literal(p):
    ''' Literal : BasicLit
                | CompositeLit '''


# BasicLit    = int_lit | float_lit | imaginary_lit | rune_lit | string_lit .
def p_BasicLit(p):
    ''' BasicLit : intLit 
                 | floatLit
                 | stringLit'''

# int_lit     = decimal_lit | octal_lit | hex_lit .
def p_intLit(p):
    ''' intLit : INTEGER'''

# float_lit = decimals "." [ decimals ] [ exponent ] |decimals exponent |"." decimals [ exponent ] .
def p_floatLit(p):
    ''' floatLit : FLOAT'''

#string_lit = raw_string_lit | interpreted_string_lit .
#may lead to conflict
def p_stringLit(p):
    ''' stringLit : STRINGVAL 
                  | CHARACTER'''


# CompositeLit  = LiteralType LiteralValue .
def p_CompositeLit(p):
    ''' CompositeLit : LiteralType LiteralValue '''


#LiteralType   = StructType | ArrayType | "[" "..." "]" ElementType |SliceType | MapType | TypeName .
def p_LiteralType(p):
    ''' LiteralType : ArrayType  '''

#TypeName = identifier | QualifiedIdent .
# def p_TypeName(p):
#     ''' TypeName : ID'''


#check for conflict here
def p_Mytypes(p):
    ''' Mytypes : BOOL 
                | BYTE 
                | INT 
                | UINT8 
                | UINT16 
                | UINT32
                | UINT64
                | INT8 
                | INT16 
                | INT32 
                | INT64 
                | UINT 
                | FLOAT32 
                | FLOAT64
                | UINTPTR 
                | STRING 
                | ERROR '''

def p_Types(p):
    ''' Types : Mytypes 
              | ID 
              | TypeLit'''

def p_Typelit(p):
    ''' TypeLit : StructType
    			| ArrayType
    			| PointerType
    			'''

def p_PointerType(p):
	'PointerType : TIMES Types'
    



def p_StructType(p):
    ''' StructType : STRUCT Repeat_multi_newline LBRACE Repeat_multi_newline  RepeatFieldDecl  RBRACE '''

def p_RepeatFieldDecl(p):
    ''' RepeatFieldDecl :  FieldDecl terminator RepeatFieldDecl
                        |  FieldDecl Repeatnewline RepeatFieldDecl 
                        |  FieldDecl
                        | FieldDecl terminator  Repeatnewline RepeatFieldDecl
                        | empty'''

def p_FieldDecl(p):
    ''' FieldDecl : IdentifierList Types
     '''


#ArrayType   = "[" ArrayLength "]" ElementType .
def p_ArrayType(p):
    ''' ArrayType :  LBRACKET Repeat_multi_newline ArrayLength RBRACKET Types'''

def p_ArrayLength(p):
    ''' ArrayLength : INTEGER '''

#LiteralValue  = "{" [ ElementList [ "," ] ] "}" .
def p_LiteralValue(p):
    ''' LiteralValue : LBRACE Repeat_multi_newline  RBRACE
                     | LBRACE Repeat_multi_newline ElementList RBRACE'''


def p_Elementlist(p):
    ''' ElementList : KeyedElement RepeatKeyedElement'''


def p_RepeatKeyedElement(p):
    ''' RepeatKeyedElement : COMMA Repeat_multi_newline KeyedElement RepeatKeyedElement
                           | empty'''


#need to remove transitivity
#KeyedElement  = [ Key ":" ] Element .
def p_KeyedElement(p):
    ''' KeyedElement : Element '''

#Element  = Expression | LiteralValue .
def p_Element(p):
    ''' Element : Expression'''

def p_empty(p):
    "empty : "
    pass

#OperandName = identifier | QualifiedIdent.
def p_OperandName(p):
    ''' OperandName : ID '''

def p_Selector(p):
    ''' Selector : PERIOD Repeat_multi_newline ID '''

def p_Index(p):
    ''' Index : LBRACKET Repeat_multi_newline Expression RBRACKET '''

#Arguments      = "(" [ ( ExpressionList | Type [ "," ExpressionList ] ) [ "..." ] [ "," ] ] ")" .
def p_Argument(p):
    ''' Arguments : LPAREN Repeat_multi_newline ExpressionList RPAREN'''

def p_IdentifierList(p):
    '''IdentifierList : ID 
                    |  ID COMMA Repeat_multi_newline IdentifierList '''



#-----------------------------------------------------------
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

filename=argv[1]
f=open(filename,'r+')
program=f.read().strip()
# program="""package main



# type person struct 
# {
#     name string;
#     age  int;
# }

# func main(e int,
#  f int ){

#   type 
#   a int
#   const a,
#   b=3,
#   4;
#   ;
#   ;
#   fmt.Println(a)

#   label:
#   a+=7

#   if a==4 {}               else {d=4}
#   switch i {
#     case 1:  fmt.Println("one")
#     case 2:
#         fmt.Println("two")
#     case 3:
#         fmt.Println("three")
#         fmt.Println("three")

#     }
#     e:=[5]int{1,2,3,4,5}

#     a='c'

  
# }

# """
yacc.parse(program, tracking = True)

