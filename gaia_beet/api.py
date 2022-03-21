__all__ = ["Gaia"]

from dataclasses import dataclass
from typing import Any, List

from beet import Context, DensityFunction, Noise

from .density_functions import DensityFunction as DF
from .density_functions import ref


@dataclass
class Gaia:
    ctx: Context
    default_namespace: str = "minecraft"

    def __id(self, id: str):
        if ":" in id:
            return id
        return f"{self.default_namespace}:{id}"

    def noise(self, id: str, first_octave: float, amplitudes: List[float]):
        self.ctx.data[self.__id(id)] = Noise(
            dict(
                firstOctave=first_octave,
                amplitudes=amplitudes,
            )
        )
        return self.__id(id)

    def df(self, id: str, function: DF):
        with self.ctx.override(gaia_default_namespace=self.default_namespace):
            content: Any = function.generate(self.ctx)
            self.ctx.data[self.__id(id)] = DensityFunction(content)
            return ref(self.__id(id))
