from beet import Context

from gaia_beet import DensityFunction as DF
from gaia_beet import Gaia


def beet_default(ctx: Context):
    gaia = ctx.inject(Gaia)

    blah = DF.slide(DF.const(2))

    foo = gaia.df("basic:foo", abs(DF.const(4) ** 3) + blah)

    gaia.df("basic:bar", blah * foo)

    gaia.df("basic:baz", DF.min(DF.const(1), DF.const(2), DF.const(3)))
