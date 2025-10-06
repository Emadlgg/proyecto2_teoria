# 🔤 Parser CYK para Gramáticas CFG

> **Proyecto 2 - Teoría de la Computación 2025**  
> Implementación del algoritmo CYK para parsing de gramáticas libres de contexto

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Descripción

Este proyecto implementa un **parser completo** para gramáticas libres de contexto (CFG) utilizando el algoritmo **CYK (Cocke-Younger-Kasami)**. El sistema puede analizar oraciones simples en inglés y determinar si son sintácticamente válidas según una gramática predefinida.

### Características principales:

✅ **Conversión automática** de gramáticas CFG a Forma Normal de Chomsky (CNF)  
✅ **Algoritmo CYK** con programación dinámica  
✅ **Construcción de árboles de parsing** (parse trees)  
✅ **Interfaz interactiva** con múltiples modos de uso  
✅ **Medición de tiempos** de ejecución  
✅ **Ejemplos predefinidos** para pruebas

---

## 🎯 Objetivos del Proyecto

- [x] Convertir una gramática CFG a su Forma Normal de Chomsky (CNF)
- [x] Implementar el algoritmo CYK para parsing
- [x] Construir árboles de parsing para sentencias válidas
- [x] Crear una interfaz de usuario interactiva
- [x] Documentar el proceso y resultados

---

## 🚀 Instalación

### Requisitos previos

- Python 3.7 o superior
- No se requieren bibliotecas externas (solo bibliotecas estándar de Python)

### Pasos de instalación

1. **Clonar o descargar** el proyecto:
```bash
git clone https://github.com/tu-usuario/cyk-parser.git
cd proyecto2_teoria
```

2. **Verificar la instalación de Python**:
```bash
python --version
# Debe mostrar Python 3.7 o superior
```

3. **Ejecutar el programa**:
```bash
python proyecto2.py
```

---

## 💻 Uso

### Inicio del Programa

Al ejecutar `proyecto2.py`, verás el menú principal:

```
======================================================================
PARSER CYK - TEORÍA DE LA COMPUTACIÓN
======================================================================

Opciones:
  1. Ver ejemplos predefinidos
  2. Ver vocabulario disponible
  3. Probar mi propia sentencia
  4. Modo interactivo (múltiples pruebas)
  5. Ver gramática en CNF
  0. Salir
======================================================================

Seleccione una opción:
```

### Opciones del Menú

#### 1️⃣ Ver ejemplos predefinidos
Ejecuta 7 ejemplos de prueba que incluyen:
- ✅ 2 sentencias semánticamente correctas
- ⚠️ 2 sentencias sintácticamente válidas pero semánticamente extrañas
- ❌ 3 sentencias no aceptadas por la gramática

**Ejemplo de salida:**
```
[Ejemplo 1]
Sentencia: 'she eats a cake'
Descripción: Semánticamente correcta
Resultado: ✓ SÍ acepta
Tiempo de ejecución: 0.000234 segundos

Árbol de Parsing:
S0
  S
    NP -> she
    VP
      V -> eats
      NP
        Det -> a
        N -> cake
```

#### 2️⃣ Ver vocabulario disponible
Muestra todas las palabras organizadas por categorías:
```
Pronombres: he, she
Determinantes: a, the
Verbos: cooks, drinks, eats, cuts
Preposiciones: in, with
Sustantivos (Animales): cat, dog
Sustantivos (Comida): beer, cake, juice, meat, soup
Sustantivos (Utensilios): fork, knife, oven, spoon
```

#### 3️⃣ Probar mi propia sentencia
Permite ingresar una sentencia personalizada:
```
Ingrese una sentencia en inglés:
> he drinks the beer

Resultado: ✓ SÍ ACEPTA
Tiempo de ejecución: 0.000189 segundos
```

#### 4️⃣ Modo interactivo
Prueba múltiples sentencias consecutivamente:
```
Sentencia #1: she eats a cake
Resultado: ✓ SÍ | Tiempo: 0.000234s
¿Ver árbol de parsing? (s/n): n

Sentencia #2: the cat quickly runs
Resultado: ✗ NO | Tiempo: 0.000156s

Sentencia #3: [Enter o 'salir' para terminar]
Total de sentencias probadas: 2
```

#### 5️⃣ Ver gramática en CNF
Muestra la gramática convertida a Forma Normal de Chomsky:
```
S0 -> S
S -> NP VP
VP -> V NP | VP PP
NP -> Det N
...
```

---

## 📖 Gramática del Lenguaje

### Estructura Básica

La gramática acepta oraciones simples con la estructura:

**S → NP VP** (Sujeto + Predicado)

Donde:
- **NP** (Noun Phrase): Sintagma nominal
- **VP** (Verb Phrase): Sintagma verbal
- **PP** (Prepositional Phrase): Sintagma preposicional

### Reglas de Producción

```
S   → NP VP
VP  → VP PP | V NP | cooks | drinks | eats | cuts
PP  → P NP
NP  → Det N | he | she
V   → cooks | drinks | eats | cuts
P   → in | with
N   → cat | dog | beer | cake | juice | meat | soup | fork | knife | oven | spoon
Det → a | the
```

### Ejemplos de Oraciones Válidas

✅ **Sintáctica y semánticamente correctas:**
- "she eats a cake"
- "he drinks the beer"
- "the cat eats the fish with a fork"

⚠️ **Sintácticamente correctas pero semánticamente extrañas:**
- "the cat cooks the soup with a dog"
- "she eats the fork"
- "he drinks the knife"

❌ **No aceptadas por la gramática:**
- "she eats" (falta objeto)
- "eats a cake" (falta sujeto)
- "the cat quickly drinks beer" (palabra no reconocida)

---

## 🏗️ Arquitectura del Proyecto

### Estructura de Archivos

```
cyk-parser/
│
├── cyk_parser.py          # Código principal
├── README.md              # Este archivo
├── informe_tecnico.md     # Documentación técnica completa
└── LICENSE                # Licencia del proyecto
```

### Componentes Principales

#### 1. **Clase CFGtoCNF**
Convierte gramáticas CFG a Forma Normal de Chomsky mediante 5 pasos:
1. Eliminar símbolo de inicio
2. Eliminar producciones epsilon
3. Eliminar producciones unitarias
4. Convertir terminales
5. Romper producciones largas

#### 2. **Clase CYKParser**
Implementa el algoritmo CYK:
- Usa programación dinámica con tabla 2D
- Complejidad: O(n³ × |G|)
- Construye parse trees mediante backpointers

#### 3. **Funciones de Interfaz**
- `show_menu()`: Menú principal
- `run_examples()`: Ejecuta ejemplos predefinidos
- `test_user_sentence()`: Prueba sentencia única
- `interactive_mode()`: Modo de pruebas múltiples
- `show_vocabulary()`: Muestra vocabulario

---

## 🧪 Ejemplos de Pruebas

### Caso 1: Sentencia válida
```python
Entrada: "she eats a cake"
Salida:  ✓ SÍ acepta
Tiempo:  0.000234 segundos
```

### Caso 2: Sentencia incompleta
```python
Entrada: "she eats"
Salida:  ✗ NO acepta
Razón:   Falta el objeto (VP requiere V NP)
```

### Caso 3: Palabra no reconocida
```python
Entrada: "she quickly eats a cake"
Salida:  ✗ NO acepta
Razón:   "quickly" no está en el vocabulario
```

---

## 📊 Rendimiento

### Complejidad Temporal

- **Conversión a CNF:** O(|G|²)
- **Algoritmo CYK:** O(n³ × |P|)
  - n = longitud de la sentencia
  - |P| = número de producciones

### Tiempos Medidos (laptop estándar)

| Longitud | Tiempo promedio |
|----------|-----------------|
| 3 palabras | ~0.0001 seg |
| 5 palabras | ~0.0003 seg |
| 7 palabras | ~0.0008 seg |

---

## 🎓 Conceptos Implementados

### Programación Dinámica
El algoritmo CYK utiliza una tabla 2D para almacenar resultados de subproblemas:
- **Subestructura óptima:** Una derivación de w[i:j] usa derivaciones de subcadenas
- **Memorización:** Evita cálculos redundantes
- **Bottom-up:** Construye soluciones desde casos base

### Forma Normal de Chomsky
Restricciones de CNF:
- A → BC (dos no-terminales)
- A → a (un terminal)
- S → ε (solo para el símbolo inicial si es necesario)

### Backpointers
Permiten reconstruir el parse tree almacenando:
- Variables que derivaron cada subcadena
- Punto de partición usado
- Referencias a subárboles izquierdo y derecho

---

## 📚 Referencias

1. **Hopcroft & Ullman** - Introduction to Automata Theory, Languages, and Computation
2. **Wikipedia** - [CYK Algorithm](https://en.wikipedia.org/wiki/CYK_algorithm)
3. **GeeksforGeeks** - [CYK Algorithm Guide](https://www.geeksforgeeks.org/cyk-algorithm-for-context-free-grammar/)
4. **UC Davis** - [CYK Notes](https://web.cs.ucdavis.edu/~rogaway/classes/120/winter12/CYK.pdf)

---

## 👨‍💻 Autores

**Osman Emanuel de León García**
**Ihan Gilberto Alexander Marroquín Sequén**

**Proyecto de Teoría de la Computación 2025**


- Universidad del Valle de Guatemala
- Curso: Teoría de la Computación
- Fecha: Octubre 2025

---



## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

---

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la documentación 
2. Verifica los ejemplos en el código
3. Abre un issue en el repositorio

---

## 🎉 Agradecimientos

Gracias a los profesores y recursos educativos que hicieron posible este proyecto.

---

**¡Feliz Parsing! 🚀**
