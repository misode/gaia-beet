from beet import Context

from gaia_beet import Gaia
from gaia_beet.density_functions import *


def beet_default(ctx: Context):
    ctx.data.pack_format = 10
    gaia = ctx.inject(Gaia)

    ZERO = gaia.df("zero", const(0))
    Y = gaia.df("y", y_clamped_gradient(-4064, 4062, -4064, 4062))
    SHIFT_X = gaia.df("shift_x", flat_cache(cache_2d(shift_a("offset"))))
    SHIFT_Z = gaia.df("shift_z", flat_cache(cache_2d(shift_b("offset"))))
    BASE_3D_NOISE = gaia.df("overworld/base_3d_noise", old_blended_noise())

    def shifted_noise_2d(noise: str):
        return flat_cache(
            shifted_noise(noise, 0.25, 0, shift_x=SHIFT_X, shift_z=SHIFT_Z)
        )

    CONTINENTS = gaia.df("overworld/continents", shifted_noise_2d("continentalness"))
    EROSION = gaia.df("overworld/erosion", shifted_noise_2d("erosion"))
    RIDGES = gaia.df("overworld/ridges", shifted_noise_2d("ridge"))
    RIDGES_FOLDED = gaia.df("overworld/ridges_folded", peaks_and_valleys(RIDGES))

    OFFSET = gaia.df(
        "overworld/offset",
        spline_with_blending(
            -0.50375 + spline(dummy_spline(CONTINENTS)), blend_offset()
        ),
    )
    FACTOR = gaia.df(
        "overworld/factor",
        spline_with_blending(spline(dummy_spline(CONTINENTS)), 10),
    )
    JAGGEDNESS = gaia.df(
        "overworld/jaggedness",
        spline_with_blending(spline(dummy_spline(CONTINENTS)), 0),
    )
    DEPTH = gaia.df("overworld/depth", y_clamped_gradient(-64, 320, 1.5, -1.5) + OFFSET)
    SLOPED_CHEESE = gaia.df(
        "overworld/sloped_cheese",
        noise_gradient_density(
            FACTOR, DEPTH + JAGGEDNESS * half_negative(noise("jagged", 1500, 0))
        )
        + BASE_3D_NOISE,
    )

    SPAGHETTI_ROUGHNESS = gaia.df(
        "overworld/caves/spaghetti_roughness_function",
        cache_once(
            mapped_noise("spaghetti_roughness_modulator", 0, -0.1)
            * (noise("spaghetti_roughness").abs() - 0.4)
        ),
    )
    SPAGHETTI_2D_THICKNESS = gaia.df(
        "overworld/caves/spaghetti_2d_thickness_modulator",
        cache_once(mapped_noise("spaghetti_2d_thickness", -0.6, -1.3, xz_scale=2)),
    )
    SPAGHETTI_2D = gaia.df(
        "overworld/caves/spaghetti_2d",
        max(
            weird_scaled_sampler(
                noise("spaghetti_2d_modulator", xz_scale=2),
                "spaghetti_2d",
                "type_2",
            )
            + 0.083 * SPAGHETTI_2D_THICKNESS,
            cube(
                abs(
                    mapped_noise("spaghetti_2d_elevation", -8, 8, y_scale=0)
                    + y_clamped_gradient(-64, 320, 8, -40)
                )
                + SPAGHETTI_2D_THICKNESS
            ),
        ).clamp(-1, 1),
    )
    caverns = add(
        noise("cave_entrance", xz_scale=0.75, y_scale=0.5),
        0.37,
        y_clamped_gradient(-10, 30, 0.3, 0),
    )
    spaghetti_rarity = cache_once(noise("spaghetti_3d_rarity", xz_scale=2))
    spaghetti = add(
        max(
            weird_scaled_sampler(spaghetti_rarity, "spaghetti_3d_1", "type_1"),
            weird_scaled_sampler(spaghetti_rarity, "spaghetti_3d_2", "type_1"),
        ),
        mapped_noise("spaghetti_3d_thickness", -0.065, -0.088),
    ).clamp(-1, 1)
    ENTRANCES = gaia.df(
        "overworld/caves/entrances",
        cache_once(min(caverns, SPAGHETTI_ROUGHNESS + spaghetti)),
    )
    NOODLE = gaia.df(
        "overworld/caves/noodle",
        range_choice(
            y_limited_interpolated(Y, noise("noodle"), -60, 320, -1),
            min=-1000000,
            max=0,
            in_range=64,
            out_of_range=add(
                y_limited_interpolated(
                    Y, mapped_noise("noodle_thickness", -0.05, -0.1), -60, 320, 0
                ),
                1.5
                * max(
                    y_limited_interpolated(
                        Y, noise("noodle_ridge_a", 8 / 3, 8 / 3), -60, 320, 0
                    ).abs(),
                    y_limited_interpolated(
                        Y, noise("noodle_ridge_b", 8 / 3, 8 / 3), -60, 320, 0
                    ).abs(),
                ),
            ),
        ),
    )
    PILLARS = gaia.df(
        "overworld/caves/pillars",
        cache_once(
            (
                noise("pillar", xz_scale=25, y_scale=0.3) * 2
                + mapped_noise("pillar_rareness", 0, -2)
            )
            * cube(mapped_noise("pillar_thickness", 0, -2))
        ),
    )


def peaks_and_valleys(input: DensityFunctionInput):
    return -3 * (-1 / 3 + abs(-2 / 3 + abs(wrap(input))))


def spline_with_blending(fn1: DensityFunctionInput, fn2: DensityFunctionInput):
    return flat_cache(cache_2d(lerp(blend_alpha(), fn2, fn1)))


def dummy_spline(continents: DensityFunction) -> Spline:
    return Spline(continents, [SplinePoint(1, 1)])


def noise_gradient_density(a: DensityFunctionInput, b: DensityFunctionInput):
    return 4 * quarter_negative(wrap(b) * a)


def y_limited_interpolated(
    input: DensityFunctionInput,
    in_range: DensityFunctionInput,
    min: float,
    max: float,
    out_of_range: DensityFunctionInput,
):
    return interpolated(range_choice(input, min, max + 1, in_range, out_of_range))
