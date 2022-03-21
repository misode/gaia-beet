from beet import Context

from gaia_beet import Gaia
from gaia_beet.density_functions import *


def beet_default(ctx: Context):
    gaia = ctx.inject(Gaia)
    gaia.default_namespace = "basic"

    blah = slide(const(2))
    foo = gaia.df("foo", abs(const(4) ** 3) + blah)
    gaia.df("bar", blah * foo)
    gaia.df("baz", min(const(1), const(2), ref("bar")))
    gaia.df("choice", range_choice(blah, 0, 64, in_range=foo))
