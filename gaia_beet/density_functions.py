from __future__ import annotations

__all__ = [
    "DensityFunction",
    "Spline",
    "SplinePoint",
    "const",
    "ref",
    "min",
    "max",
    "half_negative",
    "quarter_negative",
    "squeeze",
    "blend_alpha",
    "blend_offset",
    "blend_density",
    "beardifier",
    "old_blended_noise",
    "end_islands",
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
    "weird_scaled_sampler",
    "range_choice",
    "clamp",
    "spline",
    "terrain_shaper_spline",
]

from dataclasses import dataclass
from typing import Any, Dict, List, Literal

from beet import Context

GeneratedDensityFunction = float | str | Dict[str, Any]


class DensityFunction:
    def generate(self, ctx: Context) -> GeneratedDensityFunction:
        raise NotImplementedError("Density function generate not implemented")

    def __add__(self, other: DensityFunction):
        return TwoArgumentsDF("add", self, other)

    def __mul__(self, other: DensityFunction):
        return TwoArgumentsDF("mul", self, other)

    def __pow__(self, exp: Literal[2] | Literal[3]):
        if exp == 2:
            return OneArgument("square", self)
        elif exp == 3:
            return OneArgument("cube", self)

    def __abs__(self):
        return OneArgument("abs", self)


@dataclass
class ConstantDF(DensityFunction):
    value: float

    def generate(self, ctx: Context):
        return self.value


def const(value: float):
    return ConstantDF(value)


def ref(id: str):
    return ReferenceDF(id)


def min(*arguments: DensityFunction) -> DensityFunction:
    result = arguments[-1]
    for a in arguments[-2::-1]:
        result = TwoArgumentsDF("min", a, result)
    return result


def max(*arguments: DensityFunction) -> DensityFunction:
    result = arguments[-1]
    for a in arguments[-2::-1]:
        result = TwoArgumentsDF("max", a, result)
    return result


def half_negative(argument: DensityFunction):
    return OneArgument("half_negative", argument)


def quarter_negative(argument: DensityFunction):
    return OneArgument("quarter_negative", argument)


def squeeze(argument: DensityFunction):
    return OneArgument("squeeze", argument)


def blend_alpha():
    return NoArgumentsDF("blend_alpha")


def blend_offset():
    return NoArgumentsDF("blend_offset")


def blend_density(argument: DensityFunction):
    return OneArgument("blend_density", argument)


def beardifier():
    return NoArgumentsDF("beardifier")


def old_blended_noise():
    return NoArgumentsDF("old_blended_noise")


def end_islands():
    return NoArgumentsDF("end_islands")


def cache_2d(argument: DensityFunction):
    return OneArgument("cache_2d", argument)


def cache_all_in_cell(argument: DensityFunction):
    return OneArgument("cache_all_in_cell", argument)


def cache_once(argument: DensityFunction):
    return OneArgument("cache_once", argument)


def flat_cache(argument: DensityFunction):
    return OneArgument("flat_cache", argument)


def interpolated(argument: DensityFunction):
    return OneArgument("interpolated", argument)


def shift(argument: DensityFunction):
    return OneArgument("shift", argument)


def shift_a(argument: DensityFunction):
    return OneArgument("shift_a", argument)


def shift_b(argument: DensityFunction):
    return OneArgument("shift_b", argument)


def slide(argument: DensityFunction):
    return OneArgument("slide", argument)


def noise(noise: str, xz_scale: float = 1, y_scale: float = 1):
    return NoiseDF(noise, xz_scale, y_scale)


def shifted_noise(
    noise: str,
    xz_scale: float = 1,
    y_scale: float = 1,
    shift_x: DensityFunction = const(0),
    shift_y: DensityFunction = const(0),
    shift_z: DensityFunction = const(0),
):
    return ShiftedNoiseDF(noise, xz_scale, y_scale, shift_x, shift_y, shift_z)


def weird_scaled_sampler(
    input: DensityFunction, noise: str, rarity: Literal["type_1"] | Literal["type_2"]
):
    return WeirdScaledSamplerDF(input, noise, rarity)


def range_choice(
    input: DensityFunction,
    min: float,
    max: float,
    in_range: DensityFunction | None = None,
    out_of_range: DensityFunction | None = None,
):
    return RangeChoiceDF(input, min, max, in_range or input, out_of_range or input)


def clamp(
    input: DensityFunction,
    min: float,
    max: float,
):
    return ClampDF(input, min, max)


def spline(spline: Spline, min: float, max: float):
    return SplineDF(spline, min, max)


def terrain_shaper_spline(
    spline: Literal["offset"] | Literal["factor"] | Literal["jaggedness"],
    min: float,
    max: float,
    continentalness: DensityFunction,
    erosion: DensityFunction,
    weirdness: DensityFunction,
):
    return TerrainShaperSplineDF(spline, min, max, continentalness, erosion, weirdness)


@dataclass
class ReferenceDF(DensityFunction):
    id: str

    def generate(self, ctx: Context):
        if ":" in self.id:
            return self.id
        return f"{ctx.meta['gaia_default_namespace']}:{self.id}"


@dataclass
class NoArgumentsDF(DensityFunction):
    type: str

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:{self.type}",
        )


@dataclass
class OneArgument(DensityFunction):
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
            type=f"minecraft:shifted_noise",
            shift_x=self.shift_x.generate(ctx),
            shift_y=self.shift_y.generate(ctx),
            shift_z=self.shift_z.generate(ctx),
        )


@dataclass
class WeirdScaledSamplerDF(DensityFunction):
    input: DensityFunction
    noise: str
    type: Literal["type_1"] | Literal["type_2"]

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:weird_scaled_sampler",
            input=self.input.generate(ctx),
            noise=self.noise,
            rarity_value_mapper=self.type,
        )


class YClampedGradientDF(DensityFunction):
    from_y: int
    to_y: int
    from_value: float
    to_value: float

    def __post_init__(self):
        assert -4064 <= self.from_y <= 4062
        assert -4064 <= self.to_y <= 4062
        assert -1000000 <= self.from_value <= 1000000
        assert -1000000 <= self.to_value <= 1000000

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:y_clamped_gradient",
            from_y=self.from_y,
            to_y=self.to_y,
            from_value=self.from_value,
            to_value=self.to_value,
        )


@dataclass
class RangeChoiceDF(DensityFunction):
    input: DensityFunction
    min: float
    max: float
    in_range: DensityFunction
    out_of_range: DensityFunction

    def __post_init__(self):
        assert -1000000 <= self.min <= 1000000
        assert -1000000 <= self.max <= 1000000

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:range_choice",
            input=self.input.generate(ctx),
            min_inclusive=self.min,
            max_exclusive=self.max,
            when_in_range=self.in_range.generate(ctx),
            when_out_of_range=self.out_of_range.generate(ctx),
        )


@dataclass
class ClampDF(DensityFunction):
    input: DensityFunction
    min: float
    max: float

    def __post_init__(self):
        assert -1000000 <= self.min <= 1000000
        assert -1000000 <= self.max <= 1000000

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:clamp",
            input=self.input.generate(ctx),
            min=self.min,
            max=self.max,
        )


@dataclass
class Spline:
    coordinate: DensityFunction
    points: List[SplinePoint]

    def generate(self, ctx: Context) -> GeneratedDensityFunction:
        assert len(self.points) > 0

        return dict(
            coordinate=self.coordinate.generate(ctx),
            points=[p.generate(ctx) for p in self.points],
        )

    def add(self, location: float, value: float | Spline, derivative: float = 0):
        self.points.append(SplinePoint(location, value, derivative))
        return self


@dataclass
class SplinePoint:
    location: float
    value: float | Spline
    derivative: float = 0

    def generate(self, ctx: Context):
        if type(self.value) == float:
            value = self.value
        elif isinstance(self.value, Spline):
            value = self.value.generate(ctx)
        else:
            raise ValueError("Invalid cubic spline value")
        return dict(
            location=self.location,
            value=value,
            derivative=self.derivative,
        )


@dataclass
class SplineDF(DensityFunction):
    spline: Spline
    min: float
    max: float

    def __post_init__(self):
        assert -1000000 <= self.min <= 1000000
        assert -1000000 <= self.max <= 1000000

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:spline",
            input=self.spline.generate(ctx),
            min=self.min,
            max=self.max,
        )


@dataclass
class TerrainShaperSplineDF(DensityFunction):
    spline: Literal["offset"] | Literal["factor"] | Literal["jaggedness"]
    min: float
    max: float
    continentalness: DensityFunction
    erosion: DensityFunction
    weirdness: DensityFunction

    def __post_init__(self):
        assert -1000000 <= self.min <= 1000000
        assert -1000000 <= self.max <= 1000000

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:terrain_shaper_spline",
            spline=self.spline,
            min_value=self.min,
            max_value=self.max,
            continentalness=self.continentalness.generate(ctx),
            erosion=self.erosion.generate(ctx),
            weirdness=self.weirdness.generate(ctx),
        )
