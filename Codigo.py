import tkinter as tk
from tkinter import ttk, messagebox
from nltk import CFG, ChartParser

#Derivacion por la izquierda
def derivacionIzq(gramatica, expresion):
    """Genera la derivación por izquierda de una cadena."""
    derivacion = [] #Lista para almacenar pasos
    actual = ['E']
    derivacion.append(list(actual))# añade a la lista su valor actual
    
    while actual != expresion:
        # Buscar el primer no terminal desde la izquierda
        no_terminal_encontrado = False
        for i, simbolo in enumerate(actual): # recorre la cadena
            if simbolo in ['E', 'T', 'F']:  # si es un no terminal se deriva
                
                if simbolo == 'E':
                    if i+2 < len(expresion) and expresion[i+1] in ['+', '-']:
                        if expresion[i+1]=='+':
                            expresion[i:i+3]=['E','+','T']
                            actual.append(expresion[i:i+3])
                        elif expresion[i+1]=='-':
                            expresion[i:i+3]=['E','-','T']
                            actual.append(expresion[i:i+3])
                    else:
                        actual[i] = 'T'
                elif simbolo == 'T':
                    if i+2 < len(expresion) and expresion[i+1] in ['*', '/']:
                        if expresion[i+1]=='*':
                            expresion[i:i+3]=['T','*','F']
                            actual.append(expresion[i:i+3])
                        elif expresion[i+1]=='/':
                            expresion[i:i+3]=['T','/','F']
                            actual.append(expresion[i:i+3])
                    else:
                        actual[i] = 'F'
                elif simbolo == 'F':
                    if actual[i] == 'F': #si es terminal lo remplaza por el caracter
                        if i < len(expresion):
                            actual[i] = expresion[i]
                
                derivacion.append(list(actual))#añade el nuevo paso a la derivacion
                no_terminal_encontrado = True
                break
        
        if not no_terminal_encontrado: # si no se encuentra un no terminal,termina la derivacion
            break
    return derivacion # devuelve la lista 

#Derivacion por la derecha
def derivacionDer(gramatica, expresion):
    """Genera la derivación por derecha de una cadena."""
    derivacion = [] #Lista para almacenar pasos
    actual = ['E']
    derivacion.append(list(actual)) # añade a la lista su valor actual
    
    while actual != expresion:
        # Buscar el último no terminal desde la derecha
        no_terminal_encontrado = False
        for i in range(len(actual)-1, -1, -1): # recorre la cadena
            if actual[i] in ['E', 'T', 'F']:  # si es un no terminal deriva
                # Obtener las producciones para este no terminal
                if actual[i] == 'E':
                    if i+2 < len(expresion) and expresion[i+1] in ['+', '-']:
                        if expresion[i+1] == '+':
                            expresion[i:i+3] = ['E', '+', 'T']
                        elif expresion[i+1] == '-':
                            expresion[i:i+3] = ['E', '-', 'T']
                    else:
                        actual[i] = 'T'
                elif actual[i] == 'T':
                    if i+2 < len(actual) and actual[i+1] in ['*', '/']:
                        actual[i:i+3] = ['F']
                    else:
                        actual[i] = 'F'
                elif actual[i] == 'F':
                    if actual[i] == 'F': #si es terminal lo remplaza por el caracter
                        if i < len(expresion):
                            actual[i] = expresion[i]
                
                derivacion.append(list(actual)) #añade el nuevo paso a la derivacion
                no_terminal_encontrado = True
                break
        
        if not no_terminal_encontrado:# si no se encuentra un no terminal,termina la derivacion
            break
    return derivacion # devuelve la lista

def generar_analisis():
    #Función principal que genera derivación, árbol de derivación y AST.
    gramatica_texto = CFG.fromstring("""
    E -> E '+' T | E '-' T | T
    T -> T '*' F | T '/' F | F
    F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
""")
    expresion = entrada_expresion.get() # obtiene la opcion ingresada por el usuario
    derivacion_opcion = derivacion_var.get() # obtiene la opcion seleccionada por el usuario

    if not expresion:
        messagebox.showerror("Error", "La expresión no pueden estar vacías.") # Si esta vacio,error
        return

    
    # Generar derivación dependiendo izq-der
    if derivacion_opcion == 1:  # Izquierda
        derivacion = derivacionIzq(gramatica_texto, list(expresion))
    else:  # Derecha
        derivacion = derivacionDer(gramatica_texto, list(expresion))

    #Para mostrar la derivación   
    derivacion_texto = "\n".join(str(p) for p in derivacion)
    resultado_derivacion.set(
        f"Derivacion ({'izquierda' if derivacion_opcion ==1 else 'derecha'}): \n{derivacion_texto}"
    )

    # Generar árbol sintactico
    parser = ChartParser(gramatica_texto)
    for arbol in parser.parse(expresion):
        arbol.draw()  # Abre una ventana con el árbol sintáctico

    # Generar AST
    arbol = arbol.copy()
    for subtree in arbol.subtrees():
        if subtree.label() not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            subtree.set_label('')  
    arbol.draw()

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Análisis de Gramáticas Libres de Contexto")
ventana.geometry("500x600")

# Entradas
tk.Label(ventana, text="Gramática (formato BNF):").pack(anchor="w", padx=10, pady=5)
tk.Label(ventana, text="E -> E '+' T | E '-' T | T").pack(anchor="w", padx=10, pady=5)
tk.Label(ventana, text="T -> T '*' F | T '/' F | F").pack(anchor="w", padx=10, pady=5) 
tk.Label(ventana, text="F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p'").pack(anchor="w", padx=10, pady=5)
tk.Label(ventana, text="     | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'").pack(anchor="w", padx=10, pady=5)
tk.Label(ventana, text="     | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'").pack(anchor="w", padx=10, pady=5)

tk.Label(ventana, text="Expresión objetivo (sin espacios):").pack(anchor="w", padx=10, pady=5)
entrada_expresion = tk.Entry(ventana)
entrada_expresion.pack(fill="x", padx=10, pady=5)

tk.Label(ventana, text="Tipo de derivación:").pack(anchor="w", padx=10, pady=5)
derivacion_var = tk.IntVar(value=1)
ttk.Radiobutton(ventana, text="Izquierda", variable=derivacion_var, value=1).pack(anchor="w", padx=20)
ttk.Radiobutton(ventana, text="Derecha", variable=derivacion_var, value=2).pack(anchor="w", padx=20)

# Botón para analizar
tk.Button(ventana, text="Generar análisis", command=generar_analisis).pack(pady=10)

# Resultados
tk.Label(ventana, text="Resultado de la derivación:").pack(anchor="w", padx=10, pady=5)
resultado_derivacion = tk.StringVar()
resultado_label = tk.Label(ventana, textvariable=resultado_derivacion, justify="left", anchor="w", bg="white", relief="sunken", height=10)
resultado_label.pack(fill="both", padx=10, pady=5)

ventana.mainloop()
