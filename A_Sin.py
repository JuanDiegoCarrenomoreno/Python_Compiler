import ply.yacc as yacc
import os
import codecs
from graphviz import Source
# pip install graphviz
# https://graphviz.org/download/
import re
from A_Lex import analizador, tokens
from sys import stdin
from A_Sem import *

import tkinter as tk
from tkinter import filedialog, scrolledtext
from io import StringIO
import sys

precedence = (
    ('right','ID','CALL','BEGIN','IF','WHILE'),
    ('right','PROCEDURE'),
    ('right','VAR'),
    ('right','ASSIGN'),
    ('right','UPDATE'),
    ('left','NE'),
    ('left','LT','LTE','GT','GTE'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','ODD'),
    ('left','LPARENT','RPARENT'),
)

def p_program(p):
	'''program : block'''
	p[0] = program(p[1],"program")

def p_block(p):
    '''block : constDecl varDecl procDecl statement'''
    p[0] = block(p[1],p[2],p[3],p[4],"block")

def p_constDecl(p):
    '''constDecl : CONST constAssignmentList SEMMICOLOM'''
    p[0] = constDecl(p[2],"constDecl")

def p_constDeclEmpty(p):
    '''constDecl : empty'''
    p[0] = Null()

def p_constAssignmentList1(p):
    '''constAssignmentList : ID ASSIGN NUMBER'''
    p[0] = constAssignmentList1(Id(p[1]),Assign(p[2]),Number(p[3]),"constAssignmentList1")

def p_constAssignmentList2(p):
    '''constAssignmentList : constAssignmentList COMMA ID ASSIGN NUMBER'''
    p[0] = constAssignmentList2(p[1],Id(p[3]),Assign(p[4]),Number(p[5]),"constAssignmentList2")

def p_varDecl1(p):
    '''varDecl : VAR identList SEMMICOLOM'''
    p[0] = varDecl1(p[2],"varDecl1")

def p_varDeclEmpty(p):
    '''varDecl : empty'''
    p[0] = Null()

def p_identList1(p):
    '''identList : ID'''
    p[0] = identList1(Id(p[1]),"identList1")

def p_identList2(p):
    '''identList : identList COMMA ID'''
    p[0] = identList2(p[1],Id(p[3]),"identList2")

def p_procDecl1(p):
    '''procDecl : procDecl PROCEDURE ID SEMMICOLOM block SEMMICOLOM'''
    p[0] = procDecl1(p[1],Id(p[3]),p[5],"procDecl1")

def p_procDeclEmpty(p):
    '''procDecl : empty'''
    p[0] = Null()

def p_statement1(p):
    '''statement : ID UPDATE expression'''
    p[0] = statement1(Id(p[1]),Update(p[2]),p[3],"statement1")

def p_statement2(p):
    '''statement : CALL ID'''
    p[0] = statement2(Id(p[2]),"statement2")

def p_statement3(p):
    '''statement : BEGIN statementList END'''
    p[0] = statement3(p[2],"statement3")

def p_statement4(p):
    '''statement : IF condition THEN statement'''
    p[0] = statement4(p[2],p[4],"statement4")

def p_statement5(p):
    '''statement : WHILE condition DO statement'''
    p[0] = statement5(p[2],p[4],"statement5")

def p_statementEmpty(p):
    '''statement : empty'''
    p[0] = Null()

def p_statementList1(p):
    '''statementList : statement'''
    p[0] = statementList1(p[1],"statementList1")

def p_statementList2(p):
    '''statementList : statementList SEMMICOLOM statement'''
    p[0] = statementList2(p[1],p[3],"statementList2")

def p_condition1(p):
    '''condition : ODD expression'''
    p[0] = condition1(p[2],"condition1")

def p_condition2(p):
    '''condition : expression relation expression'''
    p[0] = condition2(p[1],p[2],p[3],"condition2")

def p_relation1(p):
    '''relation : ASSIGN'''
    p[0] = relation1(Assign(p[1]),"relation1")

def p_relation2(p):
    '''relation : NE'''
    p[0] = relation2(NE(p[1]),"relation2")

def p_relation3(p):
    '''relation : LT'''
    p[0] = relation3(LT(p[1]),"relation3")

def p_relation4(p):
    '''relation : GT'''
    p[0] = relation4(GT(p[1]),"relation4")

def p_relation5(p):
    '''relation : LTE'''
    p[0] = relation5(LTE(p[1]),"relation5")

def p_relation6(p):
    '''relation : GTE'''
    p[0] = relation6(GTE(p[1]),"relation6")

def p_expression1(p):
    '''expression : term'''
    p[0] = expression1(p[1],"expression1")

def p_expression2(p):
    '''expression : addingOperator term'''
    p[0] = expression2(p[1],p[2],"expression2")

def p_expression3(p):
    '''expression : expression addingOperator term'''
    p[0] = expression3(p[1],p[2],p[3],"expression3")

def p_addingOperator1(p):
    '''addingOperator : PLUS'''
    p[0] = addingOperator1(Plus(p[1]),"addingOperator")

def p_addingOperator2(p):
    '''addingOperator : MINUS'''
    p[0] = addingOperator2(Minus(p[1]),"subtractionOperator")

def p_term1(p):
    '''term : factor'''
    p[0] = term1(p[1],"term1")

def p_term2(p):
    '''term : term multiplyingOperator factor'''
    p[0] = term2(p[1],p[2],p[3],"term2")

def p_multiplyingOperator1(p):
    '''multiplyingOperator : TIMES'''
    p[0] = multiplyingOperator1(Times(p[1]),"multiplyingOperator")

def p_multiplyingOperator2(p):
    '''multiplyingOperator : DIVIDE'''
    p[0] = multiplyingOperator2(Divide(p[1]),"divisionOperator")

def p_factor1(p):
    '''factor : ID'''
    p[0] = factor1(Id(p[1]),"factor1")

def p_factor2(p):
    '''factor : NUMBER'''
    p[0] = factor2(Number(p[1]),"factor2")

def p_factor3(p):
    '''factor : LPARENT expression RPARENT'''
    p[0] = factor3(p[2],"factor3")

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        error_msg = f"Error de Sintaxis en '{p.value}', línea {p.lineno}\n"
    else:
        error_msg = "Error de Sintaxis: fin de entrada inesperado\n"

    imprimir_output.insert(tk.END, error_msg)

def buscarFicheros(directorio):
    ficheros = []
    numArchivo = ''
    respuesta = False
    cont = 1

    for base, dirs, files in os.walk(directorio):
        ficheros.append(files)

def traducir(result):
    graphFile = open('graphviztrhee.vz','w')
    graphFile.write(result.traducir())
    graphFile.close()
    print("El programa traducido se guardo en \"graphviztrhee.vz\"")

yacc.yacc()
parser = yacc.yacc()



#   #   #   #   #   #   GRAPHVIZ   #   #   #   #   #   #



def initialize_dot_file():
    # Ruta del archivo .dot
    dot_file_path = "output_graphviz.dot"

    # Vaciar el archivo .dot al ejecutar
    with open(dot_file_path, "w") as file:
        pass

def render_dot_file():
    dot_file_path = "output_graphviz.dot"
    
    try:
        graph = Source.from_file(dot_file_path)
        
        # Mostrar el grafico
        output_path = graph.render(filename='output_graphviz.dot', format='png', cleanup=False)
        print(f"Gráfico generado en: {output_path}")
        
        # Abrir el grafico de manera automáticamente
        os.system(f'start {output_path}')
    except FileNotFoundError:
        print(f"Error: El archivo {dot_file_path} no existe.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


#   #   #   #   #   #   INTERFAZ   #   #   #   #   #   #



root = tk.Tk()
root.title("CompilaDOOM")

def capture_output(func, *args):
    output = StringIO()
    sys.stdout = output
    func(*args)
    sys.stdout = sys.__stdout__
    return output.getvalue()

# Función para ejecutar analisis lexico y sintáctico
def run_compiler(content):
    analizador.lineno = 1
    content = content.strip()

    # Limpieza áreas de texto para antes de compilar
    lexico_output.delete(1.0, tk.END)
    imprimir_output.delete(1.0, tk.END)
    
    # Ejecucion Analisis Lexico
    analizador.input(content)
    while True:
        tok = analizador.token()
        if not tok:
            break
        lexico_output.insert(tk.END, f"{tok}\n")
    
    # Ejecucion Analisis Sintactico
    result = parser.parse(content, lexer=analizador)
    if result:
        # Mostrar el resultado de "imprimir" en la interfaz
        imprimir_result = capture_output(result.imprimir, " ")
        imprimir_output.insert(tk.END, imprimir_result)
        run_semantic_analysis(result)

        graphviz_result = result.traducir()

        # Guardar el resultado de Graphviz en un archivo
        with open("output_graphviz.dot", "w", encoding="utf-8") as file:
            file.write(graphviz_result)

    imprimir_output.insert(tk.END, result.imprimir("") + "\n")  # Mostrar árbol sintáctico

def run_semantic_analysis(result):
    semantico_output.delete(1.0, tk.END)  # Limpia la ventana de salida semántica
    variables = {}  # Diccionario para almacenar las variables y sus valores
    try:
        semantic_result = evaluate_node(result, variables)
        semantico_output.insert(tk.END, semantic_result + "\n")  # Mostrar resultados
    except Exception as e:
        semantico_output.insert(tk.END, f"Error Semántico: {e}\n")  # Mostrar errores

# Funcion para abrir y leer archivos .pl0
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PL0 Files", "*.pl0")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, content)
            run_compiler(content)

# Funcion para limpiar los datos de la ventana
def clear_all():
    input_text.delete(1.0, tk.END)
    lexico_output.delete(1.0, tk.END)
    imprimir_output.delete(1.0, tk.END)
    semantico_output.delete(1.0, tk.END)

# Funcion para ejecutar 1_9_9_3_D_O_O_M
def run_doom():
    print("Este codigo corre DOOM...")
    os.system('python __444f4f4d__/main.py')

# Texto para mostrar el archivo de entrada
label_input = tk.Label(root, text="Archivo de entrada", font=("Cambria", 12))
label_input.grid(row=0, column=0, padx=10, pady=5)
input_text = scrolledtext.ScrolledText(root, width=40, height=30)
input_text.grid(row=1, column=0, padx=10, pady=10)

# Boton para abrir archivo .pl0
open_button = tk.Button(root, text="Abrir Archivo .pl0", command=open_file, font=("Cambria", 12))
open_button.grid(row=3, column=0, columnspan=1, pady=30)

# Boton para limpiar ventana
clear_button = tk.Button(root, text="Limpiar Todo", command=clear_all, font=("Cambria", 12))
clear_button.grid(row=3, column=1, columnspan=1, pady=30)

# Boton para generar el árbol sintáctico
syntax_tree_button = tk.Button(root, text="Generar Árbol Sintáctico", command=render_dot_file, font=("Cambria", 12))
syntax_tree_button.grid(row=3, column=2, columnspan=1, pady=30)

# Boton para ejecutar 1_9_9_3_D_O_O_M
clear_button = tk.Button(root, text="Jugar DOOM", command=run_doom, font=("Cambria", 12))
clear_button.grid(row=3, column=3, columnspan=1, pady=30)

# Area de texto del resultado del analisis lexico
label_lexico = tk.Label(root, text="Análisis Léxico", font=("Cambria", 12))
label_lexico.grid(row=0, column=1, padx=10, pady=5)
lexico_output = scrolledtext.ScrolledText(root, width=40, height=30)
lexico_output.grid(row=1, column=1, padx=10, pady=10)

# Area de texto del resultado de "imprimir" arbol sintactico
label_imprimir = tk.Label(root, text="Árbol Sintáctico", font=("Cambria", 12))
label_imprimir.grid(row=0, column=2, padx=10, pady=5)
imprimir_output = scrolledtext.ScrolledText(root, width=40, height=30)
imprimir_output.grid(row=1, column=2, padx=10, pady=10)

# Area de texto del resultado del analisis semantico
label_semantico = tk.Label(root, text="Análisis Semántico", font=("Cambria", 12))
label_semantico.grid(row=0, column=3, padx=10, pady=5)
semantico_output = scrolledtext.ScrolledText(root, width=40, height=30)
semantico_output.grid(row=1, column=3, padx=10, pady=10)

#LINK Graphviz: http://www.webgraphviz.com/
initialize_dot_file()

# Ejecución
root.mainloop()