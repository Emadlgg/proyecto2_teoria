import time
from collections import defaultdict
from typing import List, Dict, Set, Tuple, Optional
import json

class CFGtoCNF:
    """Convierte una gramática CFG a Forma Normal de Chomsky (CNF)"""
    
    def __init__(self, grammar):
        self.original_grammar = grammar
        self.grammar = {}
        self.start_symbol = grammar['start']
        self.new_var_counter = 0
        
    def get_new_variable(self):
        """Genera nuevas variables para las reglas"""
        self.new_var_counter += 1
        return f"X{self.new_var_counter}"
    
    def eliminate_start_symbol(self):
        """PASO 1: Eliminar el símbolo de inicio de los lados derechos"""
        new_start = "S0"
        self.grammar[new_start] = [[self.start_symbol]]
        for var, productions in self.original_grammar['rules'].items():
            self.grammar[var] = [prod.split() for prod in productions]
        self.start_symbol = new_start
        
    def eliminate_epsilon_productions(self):
        """PASO 2: Eliminar producciones epsilon (no aplicable en esta gramática)"""
        # Esta gramática no tiene producciones epsilon, pero incluimos el método
        nullable = set()
        # Encontrar variables nullable
        changed = True
        while changed:
            changed = False
            for var, productions in self.grammar.items():
                if var not in nullable:
                    for prod in productions:
                        if all(symbol in nullable for symbol in prod):
                            nullable.add(var)
                            changed = True
                            break
        
        # Eliminar producciones epsilon y generar nuevas producciones
        if nullable:
            new_grammar = defaultdict(list)
            for var, productions in self.grammar.items():
                for prod in productions:
                    if prod != ['']:
                        # Generar todas las combinaciones sin símbolos nullable
                        self._generate_combinations(new_grammar, var, prod, nullable)
            self.grammar = dict(new_grammar)
    
    def _generate_combinations(self, new_grammar, var, prod, nullable):
        """Genera combinaciones de producción eliminando símbolos nullable"""
        new_grammar[var].append(prod)
    
    def eliminate_unit_productions(self):
        """PASO 3: Eliminar producciones unitarias (A -> B)"""
        # Encontrar pares unitarios
        unit_pairs = defaultdict(set)
        for var in self.grammar:
            unit_pairs[var].add(var)
        
        changed = True
        while changed:
            changed = False
            for var in self.grammar:
                for prod in self.grammar[var]:
                    if len(prod) == 1 and prod[0] in self.grammar:
                        # Es una producción unitaria
                        B = prod[0]
                        for C in unit_pairs[B]:
                            if C not in unit_pairs[var]:
                                unit_pairs[var].add(C)
                                changed = True
        
        # Construir nueva gramática sin producciones unitarias
        new_grammar = defaultdict(list)
        for var in self.grammar:
            for B in unit_pairs[var]:
                for prod in self.grammar[B]:
                    # Solo agregar producciones no unitarias o terminales
                    if len(prod) > 1 or prod[0] not in self.grammar:
                        if prod not in new_grammar[var]:
                            new_grammar[var].append(prod)
        
        self.grammar = dict(new_grammar)
    
    def convert_terminals(self):
        """PASO 4: Convertir terminales en producciones con variables y no-terminales"""
        new_grammar = defaultdict(list)
        terminal_vars = {}
        
        for var, productions in self.grammar.items():
            for prod in productions:
                if len(prod) == 1:
                    # Producción de un solo símbolo
                    new_grammar[var].append(prod)
                else:
                    # Producción con múltiples símbolos
                    new_prod = []
                    for symbol in prod:
                        if symbol.islower() or symbol in ['a', 'the']:
                            # Es un terminal
                            if symbol not in terminal_vars:
                                terminal_vars[symbol] = self.get_new_variable()
                                new_grammar[terminal_vars[symbol]] = [[symbol]]
                            new_prod.append(terminal_vars[symbol])
                        else:
                            new_prod.append(symbol)
                    new_grammar[var].append(new_prod)
        
        self.grammar = dict(new_grammar)
    
    def break_long_productions(self):
        """PASO 5: Romper producciones largas (más de 2 símbolos)"""
        new_grammar = defaultdict(list)
        
        for var, productions in self.grammar.items():
            for prod in productions:
                if len(prod) <= 2:
                    new_grammar[var].append(prod)
                else:
                    # Romper producción larga
                    current_var = var
                    for i in range(len(prod) - 2):
                        new_var = self.get_new_variable()
                        new_grammar[current_var].append([prod[i], new_var])
                        current_var = new_var
                    new_grammar[current_var].append(prod[-2:])
        
        self.grammar = dict(new_grammar)
    
    def convert(self):
        """Convierte la gramática completa a CNF"""
        print("Convirtiendo a Forma Normal de Chomsky...")
        self.eliminate_start_symbol()
        self.eliminate_epsilon_productions()
        self.eliminate_unit_productions()
        self.convert_terminals()
        self.break_long_productions()
        print("Conversión completada.\n")
        return {
            'start': self.start_symbol,
            'rules': self.grammar
        }


class CYKParser:
    """Implementa el algoritmo CYK para parsing de gramáticas CFG en CNF"""
    
    def __init__(self, cnf_grammar):
        self.start_symbol = cnf_grammar['start']
        self.grammar = cnf_grammar['rules']
        self.reverse_grammar = self._build_reverse_grammar()
        
    def _build_reverse_grammar(self):
        """Construye un diccionario inverso para búsqueda eficiente"""
        reverse = defaultdict(list)
        for var, productions in self.grammar.items():
            for prod in productions:
                key = tuple(prod)
                reverse[key].append(var)
        return reverse
    
    def parse(self, sentence: str) -> Tuple[bool, float, Optional[List]]:
        """
        Realiza el parsing CYK de una sentencia.
        Retorna: (acepta, tiempo, tabla_para_parse_tree)
        """
        start_time = time.time()
        
        # Tokenizar la sentencia
        words = sentence.lower().split()
        n = len(words)
        
        # Inicializar tabla dinámica (n x n x conjunto de variables)
        # table[i][j] contiene las variables que pueden derivar words[i:i+j+1]
        table = [[set() for _ in range(n)] for _ in range(n)]
        
        # Tabla para guardar backpointers (para construcción del parse tree)
        backpointer = [[defaultdict(list) for _ in range(n)] for _ in range(n)]
        
        # PASO 1: Llenar la diagonal (subcadenas de longitud 1)
        for i in range(n):
            word = words[i]
            # Buscar variables que produzcan este terminal
            for var, productions in self.grammar.items():
                for prod in productions:
                    if len(prod) == 1 and prod[0] == word:
                        table[i][0].add(var)
                        backpointer[i][0][var].append((prod[0], None, None))
        
        # PASO 2: Llenar el resto de la tabla (subcadenas de longitud 2 a n)
        for length in range(2, n + 1):  # longitud de la subcadena
            for i in range(n - length + 1):  # posición inicial
                j = length - 1  # índice en la tabla
                
                # Probar todas las particiones posibles
                for k in range(length - 1):  # punto de partición
                    # Subcadena izquierda: words[i:i+k+1]
                    # Subcadena derecha: words[i+k+1:i+length]
                    left_vars = table[i][k]
                    right_vars = table[i + k + 1][j - k - 1]
                    
                    # Buscar producciones A -> BC donde B está en left_vars y C en right_vars
                    for B in left_vars:
                        for C in right_vars:
                            key = (B, C)
                            if key in self.reverse_grammar:
                                for A in self.reverse_grammar[key]:
                                    table[i][j].add(A)
                                    backpointer[i][j][A].append((B, C, k, i, i + k + 1))
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Verificar si el símbolo de inicio está en table[0][n-1]
        accepts = self.start_symbol in table[0][n - 1]
        
        return accepts, elapsed_time, (table, backpointer, words) if accepts else None
    
    def build_parse_tree(self, parse_data) -> Dict:
        """Construye el árbol de parsing a partir de los backpointers"""
        if parse_data is None:
            return None
        
        table, backpointer, words = parse_data
        n = len(words)
        
        def build_tree(var, i, j):
            """Construye recursivamente el árbol"""
            if j == 0:  # Caso base: hoja (terminal)
                # Obtener el terminal
                for entry in backpointer[i][j][var]:
                    return {
                        'symbol': var,
                        'terminal': entry[0]
                    }
            else:
                # Caso recursivo: nodo interno
                # Tomar la primera derivación posible
                entries = backpointer[i][j][var]
                if entries:
                    B, C, k, left_start, right_start = entries[0]
                    return {
                        'symbol': var,
                        'left': build_tree(B, left_start, k),
                        'right': build_tree(C, right_start, j - k - 1)
                    }
            return None
        
        tree = build_tree(self.start_symbol, 0, n - 1)
        return tree
    
    def print_tree(self, tree, indent=0):
        """Imprime el árbol de parsing de forma legible"""
        if tree is None:
            return
        
        prefix = "  " * indent
        if 'terminal' in tree:
            print(f"{prefix}{tree['symbol']} -> {tree['terminal']}")
        else:
            print(f"{prefix}{tree['symbol']}")
            if 'left' in tree:
                self.print_tree(tree['left'], indent + 1)
            if 'right' in tree:
                self.print_tree(tree['right'], indent + 1)


def show_vocabulary(grammar):
    """Muestra el vocabulario disponible en la gramática"""
    print("\n" + "=" * 70)
    print("VOCABULARIO DISPONIBLE EN LA GRAMÁTICA")
    print("=" * 70)
    
    terminals = {
        'Pronombres': ['he', 'she'],
        'Determinantes': ['a', 'the'],
        'Verbos': ['cooks', 'drinks', 'eats', 'cuts'],
        'Preposiciones': ['in', 'with'],
        'Sustantivos (Animales)': ['cat', 'dog'],
        'Sustantivos (Comida)': ['beer', 'cake', 'juice', 'meat', 'soup'],
        'Sustantivos (Utensilios)': ['fork', 'knife', 'oven', 'spoon']
    }
    
    for category, words in terminals.items():
        print(f"\n{category}:")
        print(f"  {', '.join(words)}")
    
    print("\n" + "=" * 70)
    print("ESTRUCTURA DE ORACIONES:")
    print("  S → NP VP (Sujeto + Predicado)")
    print("  NP → Det N | Pronombre (Sintagma Nominal)")
    print("  VP → V NP | VP PP (Sintagma Verbal)")
    print("  PP → P NP (Sintagma Preposicional)")
    print("=" * 70 + "\n")


def run_examples(parser):
    """Ejecuta los ejemplos predefinidos"""
    test_sentences = [
        # Cadenas aceptadas semánticamente correctas
        ("she eats a cake", True, "Semánticamente correcta"),
        ("he drinks the beer", True, "Semánticamente correcta"),
        
        # Cadenas aceptadas pero NO semánticamente correctas
        ("the cat cooks the soup with a dog", True, "NO semánticamente correcta (gato cocinando)"),
        ("she eats the fork", True, "NO semánticamente correcta (comiendo un tenedor)"),
        
        # Cadenas NO aceptadas por la gramática
        ("she eats", False, "Incompleta - falta objeto"),
        ("eats a cake", False, "Falta sujeto"),
        ("the cat quickly drinks beer", False, "Palabra 'quickly' no está en gramática"),
    ]
    
    print("\n" + "=" * 70)
    print("EJEMPLOS PREDEFINIDOS")
    print("=" * 70 + "\n")
    
    for i, (sentence, expected, description) in enumerate(test_sentences, 1):
        print(f"[Ejemplo {i}]")
        print(f"Sentencia: '{sentence}'")
        print(f"Descripción: {description}")
        
        accepts, elapsed_time, parse_data = parser.parse(sentence)
        
        print(f"Resultado: {'✓ SÍ' if accepts else '✗ NO'} acepta")
        print(f"Tiempo de ejecución: {elapsed_time:.6f} segundos")
        
        if accepts:
            tree = parser.build_parse_tree(parse_data)
            print("\nÁrbol de Parsing:")
            parser.print_tree(tree)
        
        print("-" * 70)
        print()


def test_user_sentence(parser):
    """Permite al usuario ingresar y probar una sentencia"""
    print("\n" + "=" * 70)
    print("PROBAR SENTENCIA PERSONALIZADA")
    print("=" * 70)
    print("\nIngrese una sentencia en inglés (o presione Enter para volver):")
    print("Ejemplo: she eats a cake with a fork")
    
    sentence = input("\n> ").strip()
    
    if not sentence:
        return
    
    print(f"\nAnalizando: '{sentence}'")
    print("-" * 70)
    
    accepts, elapsed_time, parse_data = parser.parse(sentence)
    
    print(f"\nResultado: {'✓ SÍ ACEPTA' if accepts else '✗ NO ACEPTA'}")
    print(f"Tiempo de ejecución: {elapsed_time:.6f} segundos")
    
    if accepts:
        print("\n¡La sentencia es sintácticamente válida!")
        tree = parser.build_parse_tree(parse_data)
        print("\nÁrbol de Parsing:")
        parser.print_tree(tree)
    else:
        print("\n❌ La sentencia NO es válida según la gramática.")
        print("\nPosibles razones:")
        print("  • Palabras no están en el vocabulario")
        print("  • Estructura gramatical incorrecta")
        print("  • Falta sujeto o predicado")
        print("\nConsejo: Use la opción 2 para ver el vocabulario disponible.")
    
    print("\n" + "=" * 70)


def show_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 70)
    print("PARSER CYK - TEORÍA DE LA COMPUTACIÓN")
    print("=" * 70)
    print("\nOpciones:")
    print("  1. Ver ejemplos predefinidos")
    print("  2. Ver vocabulario disponible")
    print("  3. Probar mi propia sentencia")
    print("  4. Modo interactivo (múltiples pruebas)")
    print("  5. Ver gramática en CNF")
    print("  0. Salir")
    print("=" * 70)


def interactive_mode(parser):
    """Modo interactivo para múltiples pruebas"""
    print("\n" + "=" * 70)
    print("MODO INTERACTIVO")
    print("=" * 70)
    print("\nPuede probar múltiples sentencias.")
    print("Escriba 'salir' o presione Enter sin texto para terminar.\n")
    
    count = 0
    while True:
        sentence = input(f"\nSentencia #{count + 1}: ").strip()
        
        if not sentence or sentence.lower() == 'salir':
            print(f"\nTotal de sentencias probadas: {count}")
            break
        
        count += 1
        print(f"\nAnalizando: '{sentence}'")
        print("-" * 50)
        
        accepts, elapsed_time, parse_data = parser.parse(sentence)
        
        print(f"Resultado: {'✓ SÍ' if accepts else '✗ NO'} | Tiempo: {elapsed_time:.6f}s")
        
        if accepts:
            response = input("¿Ver árbol de parsing? (s/n): ").strip().lower()
            if response == 's':
                tree = parser.build_parse_tree(parse_data)
                print("\nÁrbol de Parsing:")
                parser.print_tree(tree)
        
        print("-" * 50)


def main():
    """Función principal del programa"""
    
    # Definir la gramática original
    original_grammar = {
        'start': 'S',
        'rules': {
            'S': ['NP VP'],
            'VP': ['VP PP', 'V NP', 'cooks', 'drinks', 'eats', 'cuts'],
            'PP': ['P NP'],
            'NP': ['Det N', 'he', 'she'],
            'V': ['cooks', 'drinks', 'eats', 'cuts'],
            'P': ['in', 'with'],
            'N': ['cat', 'dog', 'beer', 'cake', 'juice', 'meat', 'soup', 
                  'fork', 'knife', 'oven', 'spoon'],
            'Det': ['a', 'the']
        }
    }
    
    # Convertir a CNF
    print("\n" + "=" * 70)
    print("INICIALIZANDO PARSER CYK")
    print("=" * 70)
    converter = CFGtoCNF(original_grammar)
    cnf_grammar = converter.convert()
    
    # Crear el parser CYK
    parser = CYKParser(cnf_grammar)
    print("✓ Parser listo para usar\n")
    
    # Menú principal
    while True:
        show_menu()
        option = input("\nSeleccione una opción: ").strip()
        
        if option == '1':
            run_examples(parser)
            input("\nPresione Enter para continuar...")
            
        elif option == '2':
            show_vocabulary(original_grammar)
            input("\nPresione Enter para continuar...")
            
        elif option == '3':
            test_user_sentence(parser)
            input("\nPresione Enter para continuar...")
            
        elif option == '4':
            interactive_mode(parser)
            input("\nPresione Enter para continuar...")
            
        elif option == '5':
            print("\n" + "=" * 70)
            print("GRAMÁTICA EN FORMA NORMAL DE CHOMSKY")
            print("=" * 70 + "\n")
            for var in sorted(cnf_grammar['rules'].keys()):
                productions = cnf_grammar['rules'][var]
                prod_strs = [' '.join(prod) for prod in productions]
                print(f"{var} -> {' | '.join(prod_strs)}")
            print("\n" + "=" * 70)
            input("\nPresione Enter para continuar...")
            
        elif option == '0':
            print("\n" + "=" * 70)
            print("¡Gracias por usar el Parser CYK!")
            print("Proyecto de Teoría de la Computación 2025")
            print("=" * 70 + "\n")
            break
            
        else:
            print("\n❌ Opción inválida. Por favor, seleccione una opción del menú.")
            input("Presione Enter para continuar...")


if __name__ == "__main__":
    main()