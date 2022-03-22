from __future__ import annotations

__all__ = [
    "DensityFunction",
    "Spline",
    "SplinePoint",
    "const",
    "ref",
    "add",
    "mul",
    "min",
    "max",
    "half_negative",
    "quarter_negative",
    "square",
    "cube",
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
    "y_clamped_gradient",
    "range_choice",
    "clamp",
    "spline",
    "terrain_shaper_spline",
    "lerp",
    "map_from_unit",
    "mapped_noise",
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
            return OneArgumentDF("square", self)
        elif exp == 3:
            return OneArgumentDF("cube", self)

    def __abs__(self):
        return OneArgumentDF("abs", self)

    def clamp(self, min: float, max: float):
        return ClampDF(self, min, max)

    def abs(self):
        return OneArgumentDF("abs", self)

    @staticmethod
    def generate_id(ctx: Context, id: str):
        if ":" in id:
            return id
        return f"{ctx.meta['gaia_default_namespace']}:{id}"


@dataclass
class ConstantDF(DensityFunction):
    value: float

    def generate(self, ctx: Context):
        return self.value


def const(value: float):
    return ConstantDF(value)


def ref(id: str):
    return ReferenceDF(id)


def add(*arguments: DensityFunction) -> DensityFunction:
    assert len(arguments) > 0
    result = arguments[-1]
    for a in arguments[-2::-1]:
        result = TwoArgumentsDF("add", a, result)
    return result


def mul(*arguments: DensityFunction) -> DensityFunction:
    assert len(arguments) > 0
    result = arguments[-1]
    for a in arguments[-2::-1]:
        result = TwoArgumentsDF("mul", a, result)
    return result


def min(*arguments: DensityFunction) -> DensityFunction:
    assert len(arguments) > 0
    result = arguments[-1]
    for a in arguments[-2::-1]:
        result = TwoArgumentsDF("min", a, result)
    return result


def max(*arguments: DensityFunction) -> DensityFunction:
    assert len(arguments) > 0
    result = arguments[-1]
    for a in arguments[-2::-1]:
        result = TwoArgumentsDF("max", a, result)
    return result


def half_negative(argument: DensityFunction):
    return OneArgumentDF("half_negative", argument)


def quarter_negative(argument: DensityFunction):
    return OneArgumentDF("quarter_negative", argument)


def square(argument: DensityFunction):
    return OneArgumentDF("square", argument)


def cube(argument: DensityFunction):
    return OneArgumentDF("cube", argument)


def squeeze(argument: DensityFunction):
    return OneArgumentDF("squeeze", argument)


def blend_alpha():
    return NoArgumentsDF("blend_alpha")


def blend_offset():
    return NoArgumentsDF("blend_offset")


def blend_density(argument: DensityFunction):
    return OneArgumentDF("blend_density", argument)


def beardifier():
    return NoArgumentsDF("beardifier")


def old_blended_noise():
    return NoArgumentsDF("old_blended_noise")


def end_islands():
    return NoArgumentsDF("end_islands")


def cache_2d(argument: DensityFunction):
    return OneArgumentDF("cache_2d", argument)


def cache_all_in_cell(argument: DensityFunction):
    return OneArgumentDF("cache_all_in_cell", argument)


def cache_once(argument: DensityFunction):
    return OneArgumentDF("cache_once", argument)


def flat_cache(argument: DensityFunction):
    return OneArgumentDF("flat_cache", argument)


def interpolated(argument: DensityFunction):
    return OneArgumentDF("interpolated", argument)


def shift(noise: str):
    return ShiftNoiseDF("shift", noise)


def shift_a(noise: str):
    return ShiftNoiseDF("shift_a", noise)


def shift_b(noise: str):
    return ShiftNoiseDF("shift_b", noise)


def slide(argument: DensityFunction):
    return OneArgumentDF("slide", argument)


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


def y_clamped_gradient(from_y: int, to_y: int, from_value: float, to_value: float):
    return YClampedGradientDF(from_y, to_y, from_value, to_value)


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


def spline(spline: Spline, min: float | None = None, max: float | None = None):
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
        return self.generate_id(ctx, self.id)


@dataclass
class NoArgumentsDF(DensityFunction):
    type: str

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:{self.type}",
        )


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
class ShiftNoiseDF(DensityFunction):
    type: str
    noise_parameters: str

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:{self.type}",
            argument=self.generate_id(ctx, self.noise_parameters),
        )


@dataclass
class NoiseDF(DensityFunction):
    noise_parameters: str
    xz_scale: float
    y_scale: float

    def generate(self, ctx: Context) -> Dict[str, Any]:
        return dict(
            type=f"minecraft:noise",
            noise=self.generate_id(ctx, self.noise_parameters),
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
    noise_parameters: str
    type: Literal["type_1"] | Literal["type_2"]

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:weird_scaled_sampler",
            input=self.input.generate(ctx),
            noise=self.generate_id(ctx, self.noise_parameters),
            rarity_value_mapper=self.type,
        )


@dataclass
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
        if type(self.value) in (float, int):
            value = self.value
        elif isinstance(self.value, Spline):
            value = self.value.generate(ctx)
        else:
            raise ValueError(f"Invalid cubic spline point value {self.value}")
        return dict(
            location=self.location,
            value=value,
            derivative=self.derivative,
        )


@dataclass
class SplineDF(DensityFunction):
    spline: Spline
    min: float | None
    max: float | None

    def __post_init__(self):
        assert self.min is None or -1000000 <= self.min <= 1000000
        assert self.max is None or -1000000 <= self.max <= 1000000

    def generate(self, ctx: Context):
        if ctx.data.pack_format >= 10:
            return dict(
                type=f"minecraft:spline",
                spline=self.spline.generate(ctx),
            )
        else:
            assert (
                self.min is not None and self.max is not None
            ), f"spline min and max need to be defined for pack format {ctx.data.pack_format}"
            return dict(
                type=f"minecraft:spline",
                spline=self.spline.generate(ctx),
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
        assert ctx.data.pack_format < 10
        return dict(
            type=f"minecraft:terrain_shaper_spline",
            spline=self.spline,
            min_value=self.min,
            max_value=self.max,
            continentalness=self.continentalness.generate(ctx),
            erosion=self.erosion.generate(ctx),
            weirdness=self.weirdness.generate(ctx),
        )


def lerp(a: DensityFunction, b: DensityFunction, c: DensityFunction) -> DensityFunction:
    neg_a = const(1) + const(-1) * cache_once(a)
    return (b * neg_a) + (c * cache_once(a))


def map_from_unit(input: DensityFunction, min: float, max: float) -> DensityFunction:
    avg = const((min + max) * 0.5)
    half_diff = const((max - min) * 0.5)
    return avg + half_diff * input


def mapped_noise(
    noise: str, min: float, max: float, xz_scale: float = 1, y_scale: float = 1
) -> DensityFunction:
    return map_from_unit(NoiseDF(noise, xz_scale, y_scale), min, max)
