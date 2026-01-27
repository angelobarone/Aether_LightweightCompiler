from src.ast_nodes import NodeVisitor
import src.ast_nodes as ast
from src.tokens import TokenType

class Optimizer(NodeVisitor):

    def visit_Program(self, node):
        node.declarations = [self.visit(decl) for decl in node.declarations]
        return node

    def visit_FunctionDecl(self, node):
        node.body = self.visit(node.body)
        return node

    def visit_ExternDecl(self, node):
        return node

    def visit_Block(self, node):
        new_stmts = []
        for stmt in node.statements:
            visited = self.visit(stmt)
            if visited is not None:
                new_stmts.append(visited)
        node.statements = new_stmts
        return node

    def visit_ReturnStmt(self, node):
        node.value = self.visit(node.value)
        return node

    def visit_ExprStmt(self, node):
        node.expr = self.visit(node.expr)
        return node

    def visit_VarDecl(self, node):
        node.initializer = self.visit(node.initializer)
        return node

    def visit_IfStmt(self, node):
        node.condition = self.visit(node.condition)

        if isinstance(node.condition, ast.LiteralExpr):
            if node.condition.value != 0:
                return self.visit(node.then_branch)
            else:
                if node.else_branch:
                    return self.visit(node.else_branch)
                else:
                    return None

        node.then_branch = self.visit(node.then_branch)
        if node.else_branch:
            node.else_branch = self.visit(node.else_branch)
        return node

    def visit_WhileStmt(self, node):
        node.condition = self.visit(node.condition)

        if isinstance(node.condition, ast.LiteralExpr):
            if node.condition.value == 0:
                return None

        node.body = self.visit(node.body)
        return node

    def visit_RepeatStmt(self, node):
        node.count = self.visit(node.count)
        node.body = self.visit(node.body)
        return node

    def visit_BinaryExpr(self, node):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)

        is_left_lit = isinstance(node.left, ast.LiteralExpr)
        is_right_lit = isinstance(node.right, ast.LiteralExpr)

        if is_left_lit and is_right_lit:
            val_left = node.left.value
            val_right = node.right.value

            # Aritmetica
            if node.operator == TokenType.PLUS:
                return ast.LiteralExpr(val_left + val_right)
            elif node.operator == TokenType.MINUS:
                return ast.LiteralExpr(val_left - val_right)
            elif node.operator == TokenType.MUL:
                return ast.LiteralExpr(val_left * val_right)
            elif node.operator == TokenType.DIV:
                if val_right == 0:
                    raise ZeroDivisionError("Divisione per zero rilevata durante Constant Folding")
                return ast.LiteralExpr(int(val_left / val_right))

            # Confronti
            elif node.operator == TokenType.EQ:
                return ast.LiteralExpr(1 if val_left == val_right else 0)
            elif node.operator == TokenType.NE:
                return ast.LiteralExpr(1 if val_left != val_right else 0)
            elif node.operator == TokenType.LT:
                return ast.LiteralExpr(1 if val_left < val_right else 0)
            elif node.operator == TokenType.GT:
                return ast.LiteralExpr(1 if val_left > val_right else 0)
            elif node.operator == TokenType.LE:
                return ast.LiteralExpr(1 if val_left <= val_right else 0)
            elif node.operator == TokenType.GE:
                return ast.LiteralExpr(1 if val_left >= val_right else 0)
            elif node.operator == TokenType.AND:
                return ast.LiteralExpr(1 if (val_left and val_right) else 0)
            elif node.operator == TokenType.OR:
                return ast.LiteralExpr(1 if (val_left or val_right) else 0)

        # x + 0 -> x
        if node.operator == TokenType.PLUS:
            if is_right_lit and node.right.value == 0: return node.left
            if is_left_lit and node.left.value == 0: return node.right

        # x - 0 -> x
        if node.operator == TokenType.MINUS:
            if is_right_lit and node.right.value == 0: return node.left

        # x * 1 -> x
        if node.operator == TokenType.MUL:
            if is_right_lit and node.right.value == 1: return node.left
            if is_left_lit and node.left.value == 1: return node.right
            # x * 0 -> 0
            if is_right_lit and node.right.value == 0: return ast.LiteralExpr(0)
            if is_left_lit and node.left.value == 0: return ast.LiteralExpr(0)

        # x / 1 -> x
        if node.operator == TokenType.DIV:
            if is_right_lit and node.right.value == 1: return node.left

        return node

    def visit_UnaryExpr(self, node):
        node.operand = self.visit(node.operand)

        if isinstance(node.operand, ast.LiteralExpr):
            if node.operator == TokenType.MINUS:
                return ast.LiteralExpr(-node.operand.value)
            elif node.operator == TokenType.NOT:
                return ast.LiteralExpr(1 if node.operand.value == 0 else 0)

        return node

    def visit_LiteralExpr(self, node): return node
    def visit_VariableExpr(self, node): return node
    def visit_AssignExpr(self, node):
        node.value = self.visit(node.value)
        return node
    def visit_CallExpr(self, node):
        node.args = [self.visit(arg) for arg in node.args]
        return node
    def visit_PipeExpr(self, node):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        return node