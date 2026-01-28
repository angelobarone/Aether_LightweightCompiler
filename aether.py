import sys
import argparse
import os
from src.lexer import Lexer
from src.tokens import TokenType
from src.parser import Parser
from src.semantic_analysis import SemanticAnalyzer, SemanticError
from src.desugaring import Desugarer
from src.optimizer import Optimizer
from src.codegen import LLVMCodeGen

def get_all_tokens(lexer):
    tokens = []
    while True:
        tok = lexer.get_next_token()
        if tok.type == TokenType.EOF:
            break
        tokens.append(tok)
    return tokens

def compile_source(source_code, debug=False):
    print(f"[INFO] Avvio compilazione...")
    try:
        lexer = Lexer(source_code)
        tokens = get_all_tokens(lexer)
        if debug:
            print(f"[DEBUG] Lexer: Trovati {len(tokens)} token.")
    except Exception as e:
        print(f"[ERRORE] Lexer: {e}")
        return None

    try:
        parser = Parser(tokens)
        ast_root = parser.parse()
        if debug:
            print("[DEBUG] Parser: AST costruito con successo.")
    except Exception as e:
        print(f"[ERRORE] Parser: {e}")
        return None

    try:
        desugarer = Desugarer()
        ast_root = desugarer.visit(ast_root)
        if debug:
            print("[DEBUG] Desugaring: Zucchero sintattico rimosso.")
    except Exception as e:
        print(f"[ERRORE] Desugaring: {e}")
        return None

    try:
        analyzer = SemanticAnalyzer()
        analyzer.visit(ast_root)
        if debug:
            print("[DEBUG] Semantic Analysis: Nessun errore rilevato.")
    except SemanticError as e:
        print(f"[ERRORE] Semantica: {e}")
        return None

    try:
        optimizer = Optimizer()
        ast_root = optimizer.visit(ast_root)
        if debug:
            print("[DEBUG] Optimizer: Costanti pre-calcolate.")
    except Exception as e:
        print(f"[ERRORE] Optimizer: {e}")
        return None

    try:
        codegen = LLVMCodeGen()
        llvm_ir = codegen.generate_code(ast_root)
        print("[INFO] Generazione Codice completata.")
        return str(llvm_ir)
    except Exception as e:
        print(f"[ERRORE] CodeGen: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Compilatore MiniLang -> LLVM IR")
    parser.add_argument('input_file', help="Il file sorgente da compilare")
    parser.add_argument('-o', '--output', help="Nome del file di output (.ll)", default="output.ll")
    parser.add_argument('--debug', action='store_true', help="Stampa messaggi di debug delle fasi")

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Errore: Il file '{args.input_file}' non esiste.")
        sys.exit(1)

    with open(args.input_file, 'r') as f:
        source_code = f.read()

    llvm_result = compile_source(source_code, debug=args.debug)

    if llvm_result:
        with open(args.output, 'w') as f:
            f.write(llvm_result)
        print("------AETHER------")
        print(f"[SUCCESS] Codice LLVM IR scritto in: {args.output}")
        print("-" * 50)
        print("PER ESEGUIRE IL CODICE:")
        print(f"1. Compila il runtime C:  clang -c runtime.c -o runtime.o")
        print(f"2. Compila ed esegui:     clang {args.output} runtime.o -o programma_eseguibile")
        print(f"3. Lancia:                ./programma_eseguibile (o programma_eseguibile.exe su Windows)")
    else:
        print("[FAIL] Compilazione fallita.")
        sys.exit(1)

if __name__ == "__main__":
    main()