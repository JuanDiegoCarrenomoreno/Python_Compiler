import ply.lex as lex
import re
import codecs
import os
import sys

reservadas = ['BEGIN','END','IF','THEN','WHILE','DO','CALL','CONST',
              'VAR','PROCEDURE','OUT','IN','ELSE']

tokens = reservadas+['ID','NUMBER','PLUS','MINUS','TIMES','DIVIDE',
          'ODD','ASSIGN','NE','LT','LTE','GT','GTE',
          'LPARENT','RPARENT','COMMA','SEMMICOLOM',
          'DOT','UPDATE','SPECIAL_CHAR']

t_ignore = ' \t\r'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ODD = r'ODD'
t_ASSIGN = r'='
t_NE = r'<>'
t_LT = r'<'
t_LTE = r'<='
t_GT = r'>'
t_GTE = r'>='
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_COMMA = r','
t_SEMMICOLOM = r';'
t_DOT = r'\.'
t_UPDATE = r':='

def t_ID(t):
    r'[a-zA-Z_ñÑáéíóúÁÉÍÓÚ@#$%&¡!¿?█♂♀♠♥♣♦\x80-\xff][a-zA-Z0-9_ñÑáéíóúÁÉÍÓÚ@#$%&¡!¿?█♂♀♠♥♣♦\x80-\xff]*'
    if t.value.upper() in reservadas:
        t.value = t.value.upper()
        t.type = t.value
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    pass

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_SPECIAL_CHAR(t):
    r'[a-zA-Z_ñÑáéíóúÁÉÍÓÚ\x80-\xff][a-zA-Z0-9_ñÑáéíóúÁÉÍÓÚ\x80-\xff]*'
    print(f"Caracter Especial: '{t.value}'")
    t.type = 'SPECIAL_CHAR'
    return t

def t_error(t):
    print("Caracter Ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

analizador = lex.lex()

#   #   #   DEBBUGGER   #   #   #

#def t_error(t):
    #print(f"Caracter Ilegal '{t.value[0]}' (ASCII: {ord(t.value[0])}) en la posición {t.lexpos}")
    #t.lexer.skip(1)