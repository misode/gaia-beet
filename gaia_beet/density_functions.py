__ALL__ = ["DensityFunction"]

from dataclasses import dataclass
from typing import Any, Dict, Literal

GeneratedDensityFunction = float | str | Dict[str, Any]


class DensityFunction:
    def generate(self) -> GeneratedDensityFunction:
        raise NotImplementedError("Density function generate not implemented")

    def __add__(self, other: "DensityFunction"):
        return TwoArgumentsDF("add", self, other)

    def __mul__(self, other: "DensityFunction"):
        return TwoArgumentsDF("mul", self, other)

    def __pow__(self, exp: Literal[2] | Literal[3]):
        if exp == 2:
            return OneArgumentDF("square", self)
        elif exp == 3:
            return OneArgumentDF("cube", self)

    def __abs__(self):
        return OneArgumentDF("abs", self)

    @staticmethod
    def const(value: float):
        return ConstantDF(value)

    @staticmethod
    def ref(id: str):
        return ReferenceDF(id)

    @staticmethod
    def half_negative(argument: "DensityFunction"):
        return OneArgumentDF("half_negative", argument)

    @staticmethod
    def quarter_negative(argument: "DensityFunction"):
        return OneArgumentDF("quarter_negative", argument)

    @staticmethod
    def squeeze(argument: "DensityFunction"):
        return OneArgumentDF("squeeze", argument)

    @staticmethod
    def blend_density(argument: "DensityFunction"):
        return OneArgumentDF("blend_density", argument)

    @staticmethod
    def cache_2d(argument: "DensityFunction"):
        return OneArgumentDF("cache_2d", argument)

    @staticmethod
    def cache_all_in_cell(argument: "DensityFunction"):
        return OneArgumentDF("cache_all_in_cell", argument)

    @staticmethod
    def cache_once(argument: "DensityFunction"):
        return OneArgumentDF("cache_once", argument)

    @staticmethod
    def flat_cache(argument: "DensityFunction"):
        return OneArgumentDF("flat_cache", argument)

    @staticmethod
    def interpolated(argument: "DensityFunction"):
        return OneArgumentDF("interpolated", argument)

    @staticmethod
    def shift(argument: "DensityFunction"):
        return OneArgumentDF("shift", argument)

    @staticmethod
    def shift_a(argument: "DensityFunction"):
        return OneArgumentDF("shift_a", argument)

    @staticmethod
    def shift_b(argument: "DensityFunction"):
        return OneArgumentDF("shift_b", argument)

    @staticmethod
    def slide(argument: "DensityFunction"):
        return OneArgumentDF("slide", argument)

    @staticmethod
    def min(*arguments: "DensityFunction") -> "DensityFunction":
        result = arguments[-1]
        for a in arguments[-2::-1]:
            result = TwoArgumentsDF("min", a, result)
        return result

    @staticmethod
    def max(*arguments: "DensityFunction") -> "DensityFunction":
        result = arguments[-1]
        for a in arguments[-2::-1]:
            result = TwoArgumentsDF("max", a, result)
        return result


@dataclass
class ConstantDF(DensityFunction):
    value: float

    def generate(self):
        return self.value


@dataclass
class ReferenceDF(DensityFunction):
    id: str

    def generate(self):
        return self.id


@dataclass
class OneArgumentDF(DensityFunction):
    type: str
    argument: DensityFunction

    def generate(self):
        return {
            "type": f"minecraft:{self.type}",
            "argument": self.argument.generate(),
        }


@dataclass
class TwoArgumentsDF(DensityFunction):
    type: str
    argument1: DensityFunction
    argument2: DensityFunction

    def generate(self):
        return {
            "type": f"minecraft:{self.type}",
            "argument1": self.argument1.generate(),
            "argument2": self.argument2.generate(),
        }
