import unittest
import src.ast_nodes as ast
from src.tokens import TokenType
from src.optimizer import Optimizer

class TestOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = Optimizer()

    def test_fold_espressioni_semplici(self):
        # 3 + 4 -> 7
        expr = ast.BinaryExpr(
            left=ast.LiteralExpr(3),
            operator=TokenType.PLUS,
            right=ast.LiteralExpr(4)
        )
        res = self.optimizer.visit(expr)
        self.assertIsInstance(res, ast.LiteralExpr)
        self.assertEqual(res.value, 7)

    def test_fold_espressioni_annidate(self):
        # (10 - 2) * 3 -> 24
        inner = ast.BinaryExpr(ast.LiteralExpr(10), TokenType.MINUS, ast.LiteralExpr(2))
        outer = ast.BinaryExpr(inner, TokenType.MUL, ast.LiteralExpr(3))
        res = self.optimizer.visit(outer)
        self.assertIsInstance(res, ast.LiteralExpr)
        self.assertEqual(res.value, 24)

    def test_divisione_per_zero(self):
        # 10 / 0 -> Errore
        expr = ast.BinaryExpr(
            left=ast.LiteralExpr(10),
            operator=TokenType.DIV,
            right=ast.LiteralExpr(0)
        )
        with self.assertRaises(ZeroDivisionError):
            self.optimizer.visit(expr)

    def test_fold_confronto(self):
        # (MAGGIORE) 10 > 5 -> 1 (True)
        expr = ast.BinaryExpr(ast.LiteralExpr(10), TokenType.GT, ast.LiteralExpr(5))
        res = self.optimizer.visit(expr)
        self.assertEqual(res.value, 1)

        # (MINORE) 10 < 5 -> 0 (False)
        expr = ast.BinaryExpr(ast.LiteralExpr(10), TokenType.LT, ast.LiteralExpr(5))
        res = self.optimizer.visit(expr)
        self.assertEqual(res.value, 0)

        # (UGUAGLIANZA) 5 == 5 -> 1 (True)
        expr = ast.BinaryExpr(ast.LiteralExpr(5), TokenType.EQ, ast.LiteralExpr(5))
        res = self.optimizer.visit(expr)
        self.assertEqual(res.value, 1)

    def test_fold_logico(self):
        # (AND) 1 && 0 -> 0
        expr = ast.BinaryExpr(ast.LiteralExpr(1), TokenType.AND, ast.LiteralExpr(0))
        res = self.optimizer.visit(expr)
        self.assertEqual(res.value, 0)

        # (OR) 0 || 1 -> 1
        expr = ast.BinaryExpr(ast.LiteralExpr(0), TokenType.OR, ast.LiteralExpr(1))
        res = self.optimizer.visit(expr)
        self.assertEqual(res.value, 1)

    def test_fold_operazioni_unarie(self):
        # !0 -> 1 (Falso (0) diventa Vero (1))
        expr = ast.UnaryExpr(TokenType.NOT, ast.LiteralExpr(0))
        res = self.optimizer.visit(expr)
        self.assertEqual(res.value, 1)

        # !5 -> 0 (Vero (qualsiasi valore != 0) diventa Falso (0))
        expr = ast.UnaryExpr(TokenType.NOT, ast.LiteralExpr(5))
        res = self.optimizer.visit(expr)
        self.assertEqual(res.value, 0)

    def test_addizione_identita(self):
        # x + 0 -> x
        expr = ast.BinaryExpr(ast.VariableExpr("x"), TokenType.PLUS, ast.LiteralExpr(0))
        res = self.optimizer.visit(expr)
        self.assertIsInstance(res, ast.VariableExpr)
        self.assertEqual(res.name, "x")

        # 0 + x -> x
        expr = ast.BinaryExpr(ast.LiteralExpr(0), TokenType.PLUS, ast.VariableExpr("x"))
        res = self.optimizer.visit(expr)
        self.assertIsInstance(res, ast.VariableExpr)
        self.assertEqual(res.name, "x")

    def test_sottrazione_identita(self):
        # x - 0 -> x
        expr = ast.BinaryExpr(ast.VariableExpr("x"), TokenType.MINUS, ast.LiteralExpr(0))
        res = self.optimizer.visit(expr)
        self.assertIsInstance(res, ast.VariableExpr)
        self.assertEqual(res.name, "x")

    def test_moltiplicazione_zero(self):
        # x * 0 -> 0
        expr = ast.BinaryExpr(ast.VariableExpr("x"), TokenType.MUL, ast.LiteralExpr(0))
        res = self.optimizer.visit(expr)
        self.assertIsInstance(res, ast.LiteralExpr)
        self.assertEqual(res.value, 0)

    def test_moltiplicazione_uno(self):
        # x * 1 -> x
        expr = ast.BinaryExpr(ast.VariableExpr("x"), TokenType.MUL, ast.LiteralExpr(1))
        res = self.optimizer.visit(expr)
        self.assertIsInstance(res, ast.VariableExpr)
        self.assertEqual(res.name, "x")

    def test_divisione_uno(self):
        # x / 1 -> x
        expr = ast.BinaryExpr(ast.VariableExpr("x"), TokenType.DIV, ast.LiteralExpr(1))
        res = self.optimizer.visit(expr)
        self.assertIsInstance(res, ast.VariableExpr)
        self.assertEqual(res.name, "x")

    def test_dead_code_if_vero(self):
        # if (1) { x = 1; }
        stmt = ast.IfStmt(
            condition=ast.LiteralExpr(1),
            then_branch=ast.Block([ast.VarDecl("x", ast.LiteralExpr(1))]),
            else_branch=None
        )
        res = self.optimizer.visit(stmt)
        self.assertIsInstance(res, ast.Block)
        self.assertEqual(res.statements[0].initializer.value, 1)

    def test_dead_code_if_falso(self):
        # if (0) { x = 1; } else { x = 2; }
        stmt = ast.IfStmt(
            condition=ast.LiteralExpr(0),
            then_branch=ast.Block([ast.VarDecl("x", ast.LiteralExpr(1))]),
            else_branch=ast.Block([ast.VarDecl("x", ast.LiteralExpr(2))])
        )
        res = self.optimizer.visit(stmt)
        self.assertIsInstance(res, ast.Block)
        self.assertEqual(res.statements[0].initializer.value, 2)

    def test_dead_code_if_falso_senza_else(self):
        # if (0) { x = 1; }
        stmt = ast.IfStmt(
            condition=ast.LiteralExpr(0),
            then_branch=ast.Block([ast.VarDecl("x", ast.LiteralExpr(1))]),
            else_branch=None
        )
        res = self.optimizer.visit(stmt)
        self.assertIsNone(res)

    def test_dead_code_while_falso(self):
        # while (0) { ... }
        stmt = ast.WhileStmt(
            condition=ast.LiteralExpr(0),
            body=ast.Block([])
        )
        res = self.optimizer.visit(stmt)
        self.assertIsNone(res)

if __name__ == '__main__':
    unittest.main()