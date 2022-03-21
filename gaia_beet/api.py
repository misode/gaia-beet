__all__ = ["Gaia"]

from dataclasses import dataclass
from typing import Any

from beet import Context, DensityFunction

from .density_functions import DensityFunction as DF


@dataclass
class Gaia:
    ctx: Context

    def df(self, id: str, function: DF):
        content: Any = function.generate()
        self.ctx.data[id] = DensityFunction(content)
        return DF.ref(id)
