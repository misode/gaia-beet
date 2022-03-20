__all__ = [
    "beet_default",
]


from beet import Context, Function


def beet_default(ctx: Context):
    ctx.generate(Function(["say hello"]))
