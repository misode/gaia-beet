from beet import Context

from gaia_beet import Gaia
from gaia_beet.density_functions import *


def beet_default(ctx: Context):
    gaia = ctx.inject(Gaia)

    blah = slide(const(2))

    foo = gaia.df("basic:foo", abs(const(4) ** 3) + blah)

    gaia.df("basic:bar", blah * foo)

    gaia.df("basic:baz", min(const(1), const(2), const(3)))
