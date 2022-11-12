import ast
import logging
import math
import operator
import discord
from discord.ext import commands
from discord.ext.commands.context import Context

logger = logging.getLogger(__file__)


def safe_eval(s: str) -> float:
    """
    Evaluate a string as a mathematical expression.

    Args:
        s: The string to evaluate.

    Returns:
        The result of the evaluation.

    Raises:
        SyntaxError: If the string is not a valid mathematical expression.
    """

    def checkmath(x, *args):
        if x not in [x for x in dir(math) if not "__" in x]:
            raise SyntaxError(f"Unknown func {x}()")
        fun = getattr(math, x)
        return fun(*args)

    binOps = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.Call: checkmath,
        ast.BinOp: ast.BinOp,
    }
    unOps = {
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.UnaryOp: ast.UnaryOp,
    }
    ops = tuple(binOps) + tuple(unOps)
    tree = ast.parse(s, mode="eval")

    def _eval(node):
        if isinstance(node, ast.Expression):
            logger.debug("Expr")
            return _eval(node.body)
        elif isinstance(node, ast.Str):
            logger.debug("Str")
            return node.s
        elif isinstance(node, ast.Num):
            logger.debug("Num")
            return node.value
        elif isinstance(node, ast.Constant):
            logger.info("Const")
            return node.value
        elif isinstance(node, ast.BinOp):
            logger.debug("BinOp")
            if isinstance(node.left, ops):
                left = _eval(node.left)
            else:
                left = node.left.value
            if isinstance(node.right, ops):
                right = _eval(node.right)
            else:
                right = node.right.value
            return binOps[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            logger.debug("UpOp")
            if isinstance(node.operand, ops):
                operand = _eval(node.operand)
            else:
                operand = node.operand.value
            return unOps[type(node.op)](operand)
        elif isinstance(node, ast.Call):
            args = [_eval(x) for x in node.args]
            r = checkmath(node.func.id, *args)
            return r
        else:
            raise SyntaxError(f"Bad syntax, {type(node)}")

    return _eval(tree)


class Math(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.command(name="add", aliases=["+", "soma", "somar", "som"])
    async def add(self, ctx: Context, a: int, b: int):
        await ctx.send(str(a + b))

    @commands.command(name="sub", aliases=["-", "subtrair", "subtração"])
    async def sub(self, ctx: Context, a: int, b: int):
        await ctx.send(str(a - b))

    @commands.command(name="mult", aliases=["*", "multiplicar", "multiplicação"])
    async def mult(self, ctx: Context, a: int, b: int):
        await ctx.send(str(a * b))

    @commands.command(name="div", aliases=["/", "dividir", "divisão"])
    async def div(self, ctx: Context, a: int, b: int):
        await ctx.send(str(a / b))

    @commands.command(name="pow", aliases=["^", "potencia", "potência", "pot"])
    async def pow(self, ctx: Context, a: int, b: int):
        await ctx.send(str(a**b))

    @commands.command(
        name="sqrt", aliases=["raiz", "raiz quadrada", "raizquadrada", "raizq"]
    )
    async def sqrt(self, ctx: Context, a: int):
        await ctx.send(str(a**0.5))

    @commands.command(
        name="mod",
        aliases=[
            "%",
            "resto",
            "resto da divisão",
            "restodadivisão",
            "restodivisão",
            "resto da divisao",
            "restodadivisao",
            "restodivisao",
        ],
    )
    async def mod(self, ctx: Context, a: int, b: int):
        await ctx.send(str(a % b))

    @commands.command(name="abs", aliases=["absoluto"])
    async def abs(self, ctx: Context, a: int):
        await ctx.send(str(abs(a)))

    @commands.command(
        name="calcular", aliases=["calc", "calculadora", "calculate", "cal"]
    )
    async def calc(self, ctx: Context, *, args: str) -> None:
        """Calculates a function."""
        try:
            await ctx.send(str(safe_eval(args)))
        except Exception as e:
            await ctx.send(f"Erro ao calcular: {e}")
