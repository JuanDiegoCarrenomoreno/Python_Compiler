# Python Compiler

Compiler project developed in Python with lexical, syntactic and semantic analysis using PLY, Graphviz and Pygame.

---

## Features

* Lexical analysis
* Syntax analysis
* Semantic analysis
* Syntax tree generation
* Graph visualization
* Custom language compilation process
* Includes integration with a custom DOOM-inspired level developed for the project

---

## Technologies Used

* Python
* PLY
* Graphviz
* Pygame

---

## Project Structure

```plaintext
Compilador/
│
├── A_Lex.py          # Lexical analyzer
├── A_Sin.py          # Syntax analyzer
├── A_Sem.py          # Semantic analyzer
├── parser.out
├── parsetab.py
├── Test/
├── _444f4f4d_/       # Pygame folder
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/JuanDiegoCarrenomoreno/Python_Compiler.git
cd Python_Compiler
```

---

### 2. Install Python dependencies

```bash
pip install ply pygame graphviz
```

---

### 3. Install Graphviz

This project requires the Graphviz executable installed on the operating system.

Download Graphviz:

[https://graphviz.org/download/](https://graphviz.org/download/)

After installation, add Graphviz to the system PATH.

Example on Windows:

```plaintext
C:\Program Files\Graphviz\bin
```

If Graphviz is not added to PATH, the following error may appear:

```plaintext
failed to execute WindowsPath('dot'), make sure the Graphviz executables are on your systems' PATH
```

---

## Running the Project

The main project execution starts from the syntax analyzer module:

```bash
py A_Sin.py
```

Additional modules can also be executed individually for testing purposes:

```bash
py A_Lex.py
```

```bash
py A_Sem.py
```

---

## Requirements

* Python 3.x
* PLY
* Pygame
* Graphviz

---

## Author

Juan Diego Carreño Moreno
