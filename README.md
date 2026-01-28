# Compilatore Mini-Linguaggio (MiniLang) con Backend LLVM

**Studente:** Angelo Barone  
**Corso:** Ingegneria dei Linguaggi di Programmazione

Questo progetto implementa un compilatore completo per un linguaggio imperativo minimale ma robusto. Il sistema è scritto interamente in **Python** e genera codice intermedio **LLVM IR**, permettendo la compilazione in codice macchina.

Il compilatore include una pipeline moderna composta da: Lexer manuale, Parser ricorsivo discendente, Analisi Semantica (Scope & Arity check), Desugaring (Pipe & Repeat loop), Ottimizzatore (Constant Folding & DCE) e Code Generation.

---

## 📋 Requisiti e Dipendenze

Per eseguire il compilatore e generare gli eseguibili finali sono necessari i seguenti strumenti:

### Software Richiesto
* **Python 3.8+**: Per eseguire il compilatore.
* **Clang**: Compilatore C/C++ (parte della suite LLVM). È necessario per:
    1.  Compilare il runtime di supporto (`runtime.c`).
    2.  Effettuare il linking dell'eseguibile finale.

### Librerie Python
Il progetto dipende dalla libreria `llvmlite` per la generazione dell'IR.
  pip install llvmlite

## 📂 Struttura del Progetto
    /
    ├── main.py                   # Driver principale (Entry Point)
    ├── README.md                 # Documentazione
    ├── src/                      # Codice sorgente del compilatore
    │   ├── __init__.py
    │   ├── tokens.py             # Definizioni Token ed Enum
    │   ├── lexer.py              # Analisi Lessicale manuale
    │   ├── ast_nodes.py          # Definizione nodi AST (Dataclasses)
    │   ├── parser.py             # Analisi Sintattica Ricorsiva
    │   ├── semantic_analysis.py  # Validazione Scope e Arity
    │   ├── optimizer.py          # Constant Folding e Dead Code Elimination
    │   ├── desugaring.py         # Trasformazione AST (Repeat -> While, Pipe -> Call)
    │   └── codegen.py            # Backend LLVM IR
    └── tests/                    # Suite di test unitari
      ├── test_lexer.py
      ├── test_parser.py    
      ├── test_semantic.py
      ├── test_optimizer.py
      ├── test_desugaring.py
      └── test_codegen.py

## 🚀 Istruzioni per Build ed Esecuzione
Il processo di creazione di un eseguibile avviene in tre passaggi: compilazione del sorgente in IR, compilazione del runtime e linking finale.

### Compilazione Sorgente -> LLVM IR
Utilizza main.py per compilare un file .mini. Puoi usare il flag --debug per vedere i dettagli delle fasi intermedie.

\# Generazione del codice intermedio del programma .mini
python main.py programma.mini -o output.ll

\# Compilazione del programma
clang --target=x86_64-pc-windows-gnu -c output.ll -o output.o

\# Compilazione delle funzioni esterne di supporto .c
gcc -c runtime.c -o runtime.o

\# Linking del codice e generazione dell'eseguibile
gcc output.o runtime.o -o programma.exe

## 🧪 Testing
Il progetto include una suite di test completa basata su unittest.

Eseguire tutti i test:
 python -m unittest discover tests

## ✨ Funzionalità del Linguaggio
### Sintassi Base
    // Funzioni esterne (FFI)
    extern func print(n);

    // Funzioni utente
    func add(a, b) {
      return a + b;
    }
    
    func main() {
      let x = 10;
      let y = 20;
      
      // Pipe Operator
      let res = x |> add(y); // Equivale a add(x, y)
    
      // Repeat Loop (Zucchero sintattico)
        repeat(5) {
        print(res);
      }
    }

### Caratteristiche Tecniche
1. Tipizzazione Dinamica (Frontend) / Statica (Backend): Le variabili sono inferite, ma nel backend LLVM sono trattate come interi a 64 bit (i64).

2. Flat Scope: Le variabili definite in blocchi interni (if, while) rimangono visibili nel resto della funzione.

3. Variable Shadowing: È possibile ridichiarare una variabile con let. Questo alloca nuova memoria sullo stack, rendendo inaccessibile la precedente istanza per il resto dello scope corrente.

4. Ottimizzazioni:

Constant Folding: 3 + 4 * 2 viene compilato direttamente come 11.

Dead Code Elimination: while(0) { ... } viene rimosso completamente dall'eseguibile.

Algebraic Simplification: x * 1 diventa x, x * 0 diventa 0.

## ⚠️ Note Implementative
### Gestione Memoria:
Per semplificare la generazione del codice e supportare la mutabilità senza SSA manuale, tutte le variabili locali sono allocate sullo stack tramite istruzioni alloca.

### Compatibilità: 
Il generatore di codice inietta l'attributo "stack-probe-size"="1048576" nelle funzioni LLVM per garantire la compatibilità con l'ABI di sistema (specialmente su Windows).
