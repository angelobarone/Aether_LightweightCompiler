import unittest
import src.ast_nodes as ast
from src.semantic_analysis import SemanticAnalyzer, SemanticError

class TestSemanticAnalysis(unittest.TestCase):
    def setUp(self):
        self.analyzer = SemanticAnalyzer()

    def test_variabili_non_definite(self):
        # func main() { return x; } -> x non definito
        func = ast.FunctionDecl("main", [], ast.Block([
            ast.ReturnStmt(ast.VariableExpr("x"))
        ]))
        prog = ast.Program([func])

        with self.assertRaises(SemanticError) as cm:
            self.analyzer.visit(prog)
        self.assertIn("Variabile non definita", str(cm.exception))

    def test_arity_funzioni_interne(self):
        # func add(a, b) {} ... add(1)
        add_func = ast.FunctionDecl("add", ["a", "b"], ast.Block([]))
        call_expr = ast.CallExpr("add", [ast.LiteralExpr(1)])
        main_func = ast.FunctionDecl("main", [], ast.Block([ast.ExprStmt(call_expr)]))
        prog = ast.Program([add_func, main_func])

        with self.assertRaises(SemanticError) as cm:
            self.analyzer.visit(prog)
        self.assertIn("attesi 2 argomenti", str(cm.exception))

    def test_arity_funzioni_esterne(self):
        # extern func print(n); ... print(1, 2)
        ext = ast.ExternDecl("print", ["n"])
        call_expr = ast.CallExpr("print", [ast.LiteralExpr(1), ast.LiteralExpr(2)])
        main_func = ast.FunctionDecl("main", [], ast.Block([ast.ExprStmt(call_expr)]))
        prog = ast.Program([ext, main_func])

        with self.assertRaises(SemanticError) as cm:
            self.analyzer.visit(prog)
        self.assertIn("attesi 1 argomenti", str(cm.exception))

    def test_parametri_duplicati(self):
        # func f(x, x) {}
        func = ast.FunctionDecl("f", ["x", "x"], ast.Block([]))
        prog = ast.Program([func])

        with self.assertRaises(SemanticError) as cm:
            self.analyzer.visit(prog)
        self.assertIn("Parametro duplicato", str(cm.exception))

if __name__ == '__main__':
    unittest.main()