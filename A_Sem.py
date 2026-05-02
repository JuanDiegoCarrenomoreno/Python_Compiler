from A_Lex import tokens, analizador

txt = " "
cont = 0
def incrementarContador():
    global cont
    cont +=1
    return "%d" %cont

def process_node_for_value(node, variables):
    if isinstance(node, Number):
        return node.name
    elif isinstance(node, Id):
        if node.name in variables:
            return variables[node.name]
        else:
            raise Exception(f"Error: Variable no definida: {node.name}")
    elif isinstance(node, Assign):
        if hasattr(node, 'son1') and isinstance(node.son1, (Number, Id)):
            return process_node_for_value(node.son1, variables)
        else:
            raise Exception(f"Error: Nodo Assign inválido o sin hijo válido: {node}")
    else:
        raise Exception(f"Error: Nodo inesperado en Assign: {type(node)}")

# Función auxiliar para evaluar nodos del árbol semántico
def evaluate_node(node, variables):

    if isinstance(node, program):
        return evaluate_node(node.son1, variables)
    
    elif isinstance(node, block):
        const_result = evaluate_node(node.son1, variables) if isinstance(node.son1, constDecl) else ""
        local_variables = variables.copy()
        var_result = evaluate_node(node.son2, local_variables) if isinstance(node.son2, varDecl1) else ""
        proc_result = evaluate_node(node.son3, variables) if isinstance(node.son3, procDecl1) else ""
        instructions_result = evaluate_node(node.son4, local_variables) if node.son4 else ""
        declared_locals = {key: value for key, value in local_variables.items() if key not in variables}
        
        results = []
        if const_result:
            results.append(const_result)
        if var_result:
            if declared_locals:
                results.append(f"Variables Declaradas: {', '.join(declared_locals.keys())}")
        if proc_result:
            results.append(proc_result)
        if instructions_result:
            results.append(instructions_result)

        return "\n".join(results)

    elif isinstance(node, constDecl):

        return evaluate_node(node.son1, variables)
    

    elif isinstance(node, constAssignmentList1):

        const_name = node.son1.name
        if isinstance(node.son3, Number):  # Si es un número
            value = evaluate_expression(node.son3, variables)
        elif isinstance(node.son3, Assign):  # Si es un nodo Assign
            value = evaluate_node(node.son3, variables)
        else:
            raise Exception(f"Error: Nodo inválido en son3 de constAssignmentList1: {node.son3}")
        
        variables[const_name] = value
        return f"{const_name} = {value}"

    elif isinstance(node, constAssignmentList2):
        
        results = []
        results.append(evaluate_node(node.son1, variables))

        const_name = node.son2.name
        if isinstance(node.son3, Number):  # Si es un número
            value = evaluate_expression(node.son3, variables)
        elif isinstance(node.son3, Assign):  # Si es un nodo Assign
            value = evaluate_node(node.son3, variables)
        else:
            raise Exception(f"Error: Nodo inválido en son3 de constAssignmentList2: {node.son3}")
        
        variables[const_name] = value
        results.append(f"{const_name} = {value}")
        return "\n".join(results)

    elif isinstance(node, varDecl1):
        
        current = node.son1
        while current: 
            if isinstance(current, identList1): 
                variables[current.son1.name] = None 
                break
            elif isinstance(current, identList2):
                variables[current.son2.name] = None 
                current = current.son1
            else:
                raise Exception(f"Error: Nodo inesperado en varDecl1: {current}")
        
        return f"Variables Declaradas: {', '.join(variables.keys())}"
    
    elif isinstance(node, procDecl1):
    
        local_variables = variables.copy()   
        block_result = evaluate_node(node.son3, local_variables)
        declared_locals = {key: value for key, value in local_variables.items() if key not in variables}
        
        # Crear la salida que se imprimirá
        result = f"Procedimiento Procesado: '{node.son2.name}'\n"
        
        if declared_locals:
            result += f"Variables Declaradas: {', '.join(declared_locals.keys())}\n"
        
        result += block_result
        return result

    elif isinstance(node, Assign):
        
        if hasattr(node, 'son1') and node.son1:
            return evaluate_expression(node.son1, variables)
        else:
            raise Exception(f"Error: Nodo Assign inválido o sin hijo válido: {node}")

    elif isinstance(node, statement1):
        value = evaluate_expression(node.son3, variables)
        variables[node.son1.name] = value
        return f"{node.son1.name} := {value}"

    elif isinstance(node, statementList1):
        # Lista de una sola sentencia
        return evaluate_node(node.son1, variables)

    elif isinstance(node, statementList2): 
        # Lista de sentencias separadas por punto y coma
        result1 = evaluate_node(node.son1, variables)
        result2 = evaluate_node(node.son2, variables)
        return "\n".join(filter(None, [result1, result2]))

    elif isinstance(node, statement3):
        # BEGIN ... END
        return evaluate_node(node.son1, variables)

    elif isinstance(node, Null):
        # Nodo vacio, no hace nada
        return ""

    else:
        # Si el nodo no está manejado, lanza una excepcion
        raise Exception(f"Tipo de nodo desconocido: {type(node)}")

# Función auxiliar para evaluar expresiones
def evaluate_expression(node, variables):

    if isinstance(node, Number):  
        # Nodo que contiene un número
        return int(node.name)

    elif isinstance(node, Id):  
        # Nodo que contiene un identificador (variable)
        if node.name in variables:
            return variables[node.name] 
        else:
            raise Exception(f"Variable no definida: {node.name}")

    elif isinstance(node, expression1):  
        # Expresion simple: encapsula un termino
        return evaluate_expression(node.son1, variables)

    elif isinstance(node, expression2):  
        # Expresión con operador unario (+ o -)
        return evaluate_expression(node.son2, variables)

    elif isinstance(node, expression3):  
        # Expresión binaria: x + y, x - y, etc.
        left = evaluate_expression(node.son1, variables)  # Lado izquierdo
        operator_node = node.son2  # Nodo del operador
        right = evaluate_expression(node.son3, variables)  # Lado derecho

        # Evaluar el operador (convertir el nodo operador en un símbolo)
        if isinstance(operator_node, addingOperator1):  # +
            operator = "+"
        elif isinstance(operator_node, addingOperator2):  # -
            operator = "-"
        elif isinstance(operator_node, multiplyingOperator1):  # *
            operator = "*"
        elif isinstance(operator_node, multiplyingOperator2):  # /
            operator = "/"
        else:
            raise Exception(f"Operador desconocido: {operator_node}")

        # Realizar la operación
        if operator == "+":
            return left + right
        elif operator == "-":
            return left - right
        elif operator == "*":
            return left * right
        elif operator == "/":
            if right == 0:
                raise Exception("Error: División por cero")
            return left / right

    elif isinstance(node, term1):  
        # Término que encapsula un factor
        return evaluate_expression(node.son1, variables)

    elif isinstance(node, term2):  
        # Término con multiplicación/división
        left = evaluate_expression(node.son1, variables)
        operator = node.son2  # El nodo operador
        right = evaluate_expression(node.son3, variables)

        if isinstance(operator, multiplyingOperator1):  # Multiplicación
            return left * right
        elif isinstance(operator, multiplyingOperator2):  # División
            if right == 0:
                raise Exception("Error: División por cero")
            return left / right
        else:
            raise Exception(f"Operador desconocido: {operator}")

    elif isinstance(node, factor1):  
        # Factor que encapsula un identificador (variable)
        return evaluate_expression(node.son1, variables)

    elif isinstance(node, factor2):  
        # Factor que encapsula un número
        return evaluate_expression(node.son1, variables)

    elif isinstance(node, factor3):  
        # Factor que encapsula una expresión entre paréntesis
        return evaluate_expression(node.son1, variables)

    elif isinstance(node, addingOperator1):  
        # Este nodo ya no debería ser evaluado directamente
        raise Exception(f"Error en el flujo: Nodo addingOperator1 no debería llegar aquí.")

    elif isinstance(node, addingOperator2):  
        # Este nodo ya no debería ser evaluado directamente
        raise Exception(f"Error en el flujo: Nodo addingOperator2 no debería llegar aquí.")

    elif isinstance(node, multiplyingOperator1):  
        # Este nodo ya no debería ser evaluado directamente
        raise Exception(f"Error en el flujo: Nodo multiplyingOperator1 no debería llegar aquí.")

    elif isinstance(node, multiplyingOperator2):  
        # Este nodo ya no debería ser evaluado directamente
        raise Exception(f"Error en el flujo: Nodo multiplyingOperator2 no debería llegar aquí.")

    elif isinstance(node, Assign):
        
        if hasattr(node, 'son1') and node.son1:  # Verificar si tiene un hijo válido
            return evaluate_expression(node.son1, variables)
        else:
            raise Exception(f"Error crítico: Nodo Assign inválido: {node}")

# CLASES
class Nodo():
    pass

class Null(Nodo):
    def __init__(self):
        self.type = 'void'
    
    def imprimir(self,ident):
        return f"{ident}nodo nulo\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id+"[label = "+"nodo_nulo"+"]"+"\n\t"
        
        return id

class program(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1
    
    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt, cont
        txt=""
        cont=0
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id +"[label= "+self.name+"]"+"\n\t"

        txt += id +"->"+son1+"\n\t"
        
        return "digraph G {\n\t"+txt+"}"

class block(Nodo):
    def __init__(self,son1,son2,son3,son4,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2
        self.son3 = son3
        self.son4 = son4
    
    def imprimir(self,ident):
        result = ""
        for son in [self.son1, self.son2, self.son3, self.son4]:
            if isinstance(son, tuple):
                result += son[0].imprimir(" " + ident)
            else:
                result += son.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        if type(self.son1) == type(tuple()):
            son1 = self.son1[0].traducir()
        else:
            son1 = self.son1.traducir()
        
        if type(self.son2) == type(tuple()):
            son2 = self.son2[0].traducir()
        else:
            son2 = self.son2.traducir()
        
        if type(self.son3) == type(tuple()):
            son3 = self.son3[0].traducir()
        else:
            son3 = self.son3.traducir()
        
        if type(self.son4) == type(tuple()):
            son4 = self.son4[0].traducir()
        else:
            son4 = self.son4.traducir()
        
        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"
        txt += id + " -> " + son3 + "\n\t"
        txt += id + " -> " + son4 + "\n\t"

        return id

class constDecl(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1
    
    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        if type(self.son1) == type(tuple()):
            son1 = self.son1[0].traducir()
        else:
            son1 = self.son1.traducir()

        txt += id +"[label= "+self.name+"]"+"\n\t"
        txt += id +"->"+son1+"\n\t"

        return id

class constAssignmentList1(Nodo):
    def __init__(self,son1,son2,son3,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2
        self.son3 = son3
    
    def imprimir(self,ident):
        result = ""
        result += self.son1.imprimir(" " + ident)
        result += self.son2.imprimir(" " + ident)
        result += self.son3.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        son3 = self.son3.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"
        txt += id + " -> " + son3 + "\n\t"

        return id

class constAssignmentList2(Nodo):
    def __init__(self,son1,son2,son3,son4,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2
        self.son3 = son3
        self.son4 = son4

    def imprimir(self,ident):
        result = ""
        result += self.son1.imprimir(" " + ident)
        result += self.son2.imprimir(" " + ident)
        result += self.son3.imprimir(" " + ident)
        result += self.son4.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        son3 = self.son3.traducir()
        son4 = self.son4.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"
        txt += id + " -> " + son3 + "\n\t"
        txt += id + " -> " + son4 + "\n\t"

        return id

class varDecl1(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1
    
    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class identList1(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1
    
    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class identList2(Nodo):
    def __init__(self,son1,son2,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2
    
    def imprimir(self,ident):
        result = ""
        result += self.son1.imprimir(" " + ident)
        result += self.son2.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"

        return id

class procDecl1(Nodo):
    def __init__(self,son1,son2,son3,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2
        self.son3 = son3
    
    def imprimir(self,ident):
        result = ""
        # Procesar son1, verificando si es una tupla
        if isinstance(self.son1, tuple):
            result += self.son1[0].imprimir(" " + ident)
        else:
            result += self.son1.imprimir(" " + ident)
        # Procesar son2 y son3
        result += self.son2.imprimir(" " + ident)
        result += self.son3.imprimir(" " + ident)
        # Agregar el nodo actual
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        son3 = self.son3.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"
        txt += id + " -> " + son3 + "\n\t"

        return id

class statement1(Nodo):
    def __init__(self,son1,son2,son3,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2
        self.son3 = son3
    
    def imprimir(self,ident):
        result = ""
        result += self.son1.imprimir(" " + ident)
        result += self.son2.imprimir(" " + ident)
        result += self.son3.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        son3 = self.son3.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"
        txt += id + " -> " + son3 + "\n\t"

        return id

class statement2(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1
    
    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class statement3(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1
    
    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class statement4(Nodo):
    def __init__(self,son1,son2,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2


    def imprimir(self,ident):
        result = ""
        # Procesar son1
        result += self.son1.imprimir(" " + ident)
        # Procesar son2, verificando si es una tupla
        if isinstance(self.son2, tuple):
            result += self.son2[0].imprimir(" " + ident)
        else:
            result += self.son2.imprimir(" " + ident)
        # Agregar el nodo actual
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"

        return id

class statement5(Nodo):
    def __init__(self,son1,son2,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self,ident):
        result = ""
        # Procesar son1
        result += self.son1.imprimir(" " + ident)
        # Procesar son2, verificando si es una tupla
        if isinstance(self.son2, tuple):
            result += self.son2[0].imprimir(" " + ident)
        else:
            result += self.son2.imprimir(" " + ident)
        # Agregar el nodo actual
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"

        return id

class statementList1(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class statementList2(Nodo):
    def __init__(self,son1,son2,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self,ident):
        result = ""
        result += self.son1.imprimir(" " + ident)
        result += self.son2.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"

        return id

class condition1(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class condition2(Nodo):
    def __init__(self,son1,son2,son3,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2
        self.son3 = son3

    def imprimir(self,ident):
        result = ""
        result += self.son1.imprimir(" " + ident)
        result += self.son2.imprimir(" " + ident)
        result += self.son3.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        son3 = self.son3.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"
        txt += id + " -> " + son3 + "\n\t"

        return id

class relation1(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class relation2(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class relation3(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class relation4(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class relation5(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class relation6(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class expression1(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class expression2(Nodo):
    def __init__(self,son1,son2,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2

    def imprimir(self,ident):
        result = ""
        result += self.son1.imprimir(" " + ident)
        result += self.son2.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"

        return id

class expression3(Nodo):
    def __init__(self,son1,son2,son3,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2
        self.son3 = son3

    def imprimir(self,ident):
        result = ""
        result += self.son1.imprimir(" " + ident)
        result += self.son2.imprimir(" " + ident)
        result += self.son3.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        son3 = self.son3.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"
        txt += id + " -> " + son3 + "\n\t"

        return id

class addingOperator1(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class addingOperator2(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class term1(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class term2(Nodo):
    def __init__(self,son1,son2,son3,name):
        self.name = name
        self.son1 = son1
        self.son2 = son2
        self.son3 = son3

    def imprimir(self,ident):
        result = ""
        result += self.son1.imprimir(" " + ident)
        result += self.son2.imprimir(" " + ident)
        result += self.son3.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()
        son2 = self.son2.traducir()
        son3 = self.son3.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"
        txt += id + " -> " + son2 + "\n\t"
        txt += id + " -> " + son3 + "\n\t"

        return id

class multiplyingOperator1(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class multiplyingOperator2(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class factor1(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class factor2(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id

class factor3(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.son1 = son1

    def imprimir(self,ident):
        result = self.son1.imprimir(" " + ident)
        result += f"{ident}Nodo: {self.name}\n"
        return result

    def traducir(self):
        global txt
        id = incrementarContador()

        son1 = self.son1.traducir()

        txt += id + "[label= "+self.name+"]"+"\n\t"
        txt += id + " -> " + son1 + "\n\t"

        return id


#   #   #   #   #   #   #   #   #   #   #   #   #   #


class Id(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        return f"{ident}ID: {self.name}\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= "+self.name+"]"+"\n\t"

        return id

class Assign(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        return f"{ident}Assign: {self.name}\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class NE(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        return f"{ident}NE: {self.name}\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class LT(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        return f"{ident}LT: {self.name}\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class GT(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        return f"{ident}GT: {self.name}\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class LTE(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        return f"{ident}LTE: {self.name}\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class GTE(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        return f"{ident}GTE: {self.name}\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class Plus(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        return f"{ident}Plus: {self.name}\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class Minus(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        return f"{ident}Minus: {self.name}\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class Times(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        return f"{ident}Times: {self.name}\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"

        return id

class Divide(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        return f"{ident}Divide: {self.name}\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"
        return id

class Update(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        return f"{ident}Update: {self.name}\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= \""+self.name+"\"]"+"\n\t"
        return id

class Number(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(self,ident):
        return f"{ident}Number: {self.name}\n"

    def traducir(self):
        global txt
        id = incrementarContador()
        txt += id + "[label= "+str(self.name)+"]"+"\n\t"
        return id
