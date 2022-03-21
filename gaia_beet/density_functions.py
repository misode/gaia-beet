__all__ = [
    "DensityFunction",
    "const",
    "ref",
    "min",
    "max",
    "half_negative",
    "quarter_negative",
    "squeeze",
    "blend_density",
    "cache_2d",
    "cache_all_in_cell",
    "cache_once",
    "flat_cache",
    "interpolated",
    "shift",
    "shift_a",
    "shift_b",
    "slide",
    "noise",
    "shifted_noise",
]

from dataclasses import dataclass
from typing import Any, Dict, Literal

from beet import Context

GeneratedDensityFunction = float | str | Dict[str, Any]


class DensityFunction:
    def generate(self, ctx: Context) -> GeneratedDensityFunction:
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


@dataclass
class ConstantDF(DensityFunction):
    value: float

    def generate(self, ctx: Context):
        return self.value


def const(value: float):
    return ConstantDF(value)


def ref(id: str):
    return ReferenceDF(id)


def min(*arguments: "DensityFunction") -> "DensityFunction":
    result = arguments[-1]
    for a in arguments[-2::-1]:
        result = TwoArgumentsDF("min", a, result)
    return result


def max(*arguments: "DensityFunction") -> "DensityFunction":
    result = arguments[-1]
    for a in arguments[-2::-1]:
        result = TwoArgumentsDF("max", a, result)
    return result


def half_negative(argument: "DensityFunction"):
    return OneArgumentDF("half_negative", argument)


def quarter_negative(argument: "DensityFunction"):
    return OneArgumentDF("quarter_negative", argument)


def squeeze(argument: "DensityFunction"):
    return OneArgumentDF("squeeze", argument)


def blend_density(argument: "DensityFunction"):
    return OneArgumentDF("blend_density", argument)


def cache_2d(argument: "DensityFunction"):
    return OneArgumentDF("cache_2d", argument)


def cache_all_in_cell(argument: "DensityFunction"):
    return OneArgumentDF("cache_all_in_cell", argument)


def cache_once(argument: "DensityFunction"):
    return OneArgumentDF("cache_once", argument)


def flat_cache(argument: "DensityFunction"):
    return OneArgumentDF("flat_cache", argument)


def interpolated(argument: "DensityFunction"):
    return OneArgumentDF("interpolated", argument)


def shift(argument: "DensityFunction"):
    return OneArgumentDF("shift", argument)


def shift_a(argument: "DensityFunction"):
    return OneArgumentDF("shift_a", argument)


def shift_b(argument: "DensityFunction"):
    return OneArgumentDF("shift_b", argument)


def slide(argument: "DensityFunction"):
    return OneArgumentDF("slide", argument)


def noise(noise: str, xz_scale: float = 1, y_scale: float = 1):
    return NoiseDF(noise, xz_scale, y_scale)


def shifted_noise(
    noise: str,
    xz_scale: float = 1,
    y_scale: float = 1,
    shift_x: "DensityFunction" = const(0),
    shift_y: "DensityFunction" = const(0),
    shift_z: "DensityFunction" = const(0),
):
    return ShiftedNoiseDF(noise, xz_scale, y_scale, shift_x, shift_y, shift_z)


@dataclass
class ReferenceDF(DensityFunction):
    id: str

    def generate(self, ctx: Context):
        return self.id


@dataclass
class OneArgumentDF(DensityFunction):
    type: str
    argument: DensityFunction

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:{self.type}",
            argument=self.argument.generate(ctx),
        )


@dataclass
class TwoArgumentsDF(DensityFunction):
    type: str
    argument1: DensityFunction
    argument2: DensityFunction

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:{self.type}",
            argument1=self.argument1.generate(ctx),
            argument2=self.argument2.generate(ctx),
        )


@dataclass
class NoiseDF(DensityFunction):
    noise_parameters: str
    xz_scale: float
    y_scale: float

    def generate(self, ctx: Context) -> Dict[str, Any]:
        return dict(
            type=f"minecraft:noise",
            noise=self.noise_parameters,
            xz_scale=self.xz_scale,
            y_scale=self.y_scale,
        )


@dataclass
class ShiftedNoiseDF(NoiseDF):
    shift_x: DensityFunction
    shift_y: DensityFunction
    shift_z: DensityFunction

    def generate(self, ctx: Context):
        return dict(
            super().generate(ctx),
            shift_x=self.shift_x.generate(ctx),
            shift_y=self.shift_y.generate(ctx),
            shift_z=self.shift_z.generate(ctx),
        )
