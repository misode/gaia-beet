__all__ = ["Gaia"]

from dataclasses import dataclass
from typing import Any, List

from beet import Context, DensityFunction, Noise

from .density_functions import DensityFunction as DF
from .density_functions import ref


@dataclass
class Gaia:
    ctx: Context

    def noise(self, id: str, first_octave: float, amplitudes: List[float]):
        self.ctx.data[id] = Noise(
            {
                "firstOctave": first_octave,
                "amplitudes": amplitudes,
            }
        )
        return id

    def df(self, id: str, function: DF):
        content: Any = function.generate(self.ctx)
        self.ctx.data[id] = DensityFunction(content)
        return ref(id)
