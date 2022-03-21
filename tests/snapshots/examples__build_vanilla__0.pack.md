# Lectern snapshot

## Data pack

`@data_pack pack.mcmeta`

```json
{
  "pack": {
    "pack_format": 10,
    "description": ""
  }
}
```

### minecraft

`@density_function minecraft:zero`

```json
0
```

`@density_function minecraft:y`

```json
{
  "type": "minecraft:y_clamped_gradient",
  "from_y": -4064,
  "to_y": 4062,
  "from_value": -4064,
  "to_value": 4062
}
```

`@density_function minecraft:shift_x`

```json
{
  "type": "minecraft:flat_cache",
  "argument": {
    "type": "minecraft:cache_2d",
    "argument": {
      "type": "minecraft:shift_a",
      "argument": "minecraft:offset"
    }
  }
}
```

`@density_function minecraft:shift_z`

```json
{
  "type": "minecraft:flat_cache",
  "argument": {
    "type": "minecraft:cache_2d",
    "argument": {
      "type": "minecraft:shift_b",
      "argument": "minecraft:offset"
    }
  }
}
```

`@density_function minecraft:overworld/base_3d_noise`

```json
{
  "type": "minecraft:old_blended_noise"
}
```

`@density_function minecraft:overworld/continents`

```json
{
  "type": "minecraft:flat_cache",
  "argument": {
    "type": "minecraft:shifted_noise",
    "noise": "minecraft:continentalness",
    "xz_scale": 0.25,
    "y_scale": 0,
    "shift_x": "minecraft:shift_x",
    "shift_y": 0,
    "shift_z": "minecraft:shift_z"
  }
}
```

`@density_function minecraft:overworld/erosion`

```json
{
  "type": "minecraft:flat_cache",
  "argument": {
    "type": "minecraft:shifted_noise",
    "noise": "minecraft:erosion",
    "xz_scale": 0.25,
    "y_scale": 0,
    "shift_x": "minecraft:shift_x",
    "shift_y": 0,
    "shift_z": "minecraft:shift_z"
  }
}
```

`@density_function minecraft:overworld/ridges`

```json
{
  "type": "minecraft:flat_cache",
  "argument": {
    "type": "minecraft:shifted_noise",
    "noise": "minecraft:ridge",
    "xz_scale": 0.25,
    "y_scale": 0,
    "shift_x": "minecraft:shift_x",
    "shift_y": 0,
    "shift_z": "minecraft:shift_z"
  }
}
```

`@density_function minecraft:overworld/ridges_folded`

```json
{
  "type": "minecraft:mul",
  "argument1": -3,
  "argument2": {
    "type": "minecraft:add",
    "argument1": -0.3333333333333333,
    "argument2": {
      "type": "minecraft:abs",
      "argument": {
        "type": "minecraft:add",
        "argument1": -0.6666666666666666,
        "argument2": {
          "type": "minecraft:abs",
          "argument": "minecraft:overworld/ridges"
        }
      }
    }
  }
}
```

`@density_function minecraft:overworld/offset`

```json
{
  "type": "minecraft:flat_cache",
  "argument": {
    "type": "minecraft:cache_2d",
    "argument": {
      "type": "minecraft:add",
      "argument1": {
        "type": "minecraft:mul",
        "argument1": {
          "type": "minecraft:blend_offset"
        },
        "argument2": {
          "type": "minecraft:add",
          "argument1": 1,
          "argument2": {
            "type": "minecraft:mul",
            "argument1": -1,
            "argument2": {
              "type": "minecraft:cache_once",
              "argument": {
                "type": "minecraft:blend_alpha"
              }
            }
          }
        }
      },
      "argument2": {
        "type": "minecraft:mul",
        "argument1": {
          "type": "minecraft:add",
          "argument1": -0.50375,
          "argument2": {
            "type": "minecraft:spline",
            "spline": {
              "coordinate": "minecraft:overworld/continents",
              "points": [
                {
                  "location": 1,
                  "value": 1,
                  "derivative": 0
                }
              ]
            }
          }
        },
        "argument2": {
          "type": "minecraft:cache_once",
          "argument": {
            "type": "minecraft:blend_alpha"
          }
        }
      }
    }
  }
}
```

`@density_function minecraft:overworld/factor`

```json
{
  "type": "minecraft:flat_cache",
  "argument": {
    "type": "minecraft:cache_2d",
    "argument": {
      "type": "minecraft:add",
      "argument1": {
        "type": "minecraft:mul",
        "argument1": 10,
        "argument2": {
          "type": "minecraft:add",
          "argument1": 1,
          "argument2": {
            "type": "minecraft:mul",
            "argument1": -1,
            "argument2": {
              "type": "minecraft:cache_once",
              "argument": {
                "type": "minecraft:blend_alpha"
              }
            }
          }
        }
      },
      "argument2": {
        "type": "minecraft:mul",
        "argument1": {
          "type": "minecraft:spline",
          "spline": {
            "coordinate": "minecraft:overworld/continents",
            "points": [
              {
                "location": 1,
                "value": 1,
                "derivative": 0
              }
            ]
          }
        },
        "argument2": {
          "type": "minecraft:cache_once",
          "argument": {
            "type": "minecraft:blend_alpha"
          }
        }
      }
    }
  }
}
```

`@density_function minecraft:overworld/jaggedness`

```json
{
  "type": "minecraft:flat_cache",
  "argument": {
    "type": "minecraft:cache_2d",
    "argument": {
      "type": "minecraft:add",
      "argument1": {
        "type": "minecraft:mul",
        "argument1": 0,
        "argument2": {
          "type": "minecraft:add",
          "argument1": 1,
          "argument2": {
            "type": "minecraft:mul",
            "argument1": -1,
            "argument2": {
              "type": "minecraft:cache_once",
              "argument": {
                "type": "minecraft:blend_alpha"
              }
            }
          }
        }
      },
      "argument2": {
        "type": "minecraft:mul",
        "argument1": {
          "type": "minecraft:spline",
          "spline": {
            "coordinate": "minecraft:overworld/continents",
            "points": [
              {
                "location": 1,
                "value": 1,
                "derivative": 0
              }
            ]
          }
        },
        "argument2": {
          "type": "minecraft:cache_once",
          "argument": {
            "type": "minecraft:blend_alpha"
          }
        }
      }
    }
  }
}
```

`@density_function minecraft:overworld/depth`

```json
{
  "type": "minecraft:add",
  "argument1": {
    "type": "minecraft:y_clamped_gradient",
    "from_y": -64,
    "to_y": 320,
    "from_value": 1.5,
    "to_value": -1.5
  },
  "argument2": "minecraft:overworld/offset"
}
```

`@density_function minecraft:overworld/sloped_cheese`

```json
{
  "type": "minecraft:add",
  "argument1": {
    "type": "minecraft:mul",
    "argument1": 4,
    "argument2": {
      "type": "minecraft:quarter_negative",
      "argument": {
        "type": "minecraft:mul",
        "argument1": {
          "type": "minecraft:add",
          "argument1": "minecraft:overworld/depth",
          "argument2": {
            "type": "minecraft:mul",
            "argument1": "minecraft:overworld/jaggedness",
            "argument2": {
              "type": "minecraft:half_negative",
              "argument": {
                "type": "minecraft:noise",
                "noise": "minecraft:jagged",
                "xz_scale": 1500,
                "y_scale": 0
              }
            }
          }
        },
        "argument2": "minecraft:overworld/factor"
      }
    }
  },
  "argument2": "minecraft:overworld/base_3d_noise"
}
```

`@density_function minecraft:overworld/caves/spaghetti_roughness_function`

```json
{
  "type": "minecraft:cache_once",
  "argument": {
    "type": "minecraft:mul",
    "argument1": {
      "type": "minecraft:add",
      "argument1": -0.05,
      "argument2": {
        "type": "minecraft:mul",
        "argument1": -0.05,
        "argument2": {
          "type": "minecraft:noise",
          "noise": "minecraft:spaghetti_roughness_modulator",
          "xz_scale": 1,
          "y_scale": 1
        }
      }
    },
    "argument2": {
      "type": "minecraft:add",
      "argument1": {
        "type": "minecraft:abs",
        "argument": {
          "type": "minecraft:noise",
          "noise": "minecraft:spaghetti_roughness",
          "xz_scale": 1,
          "y_scale": 1
        }
      },
      "argument2": -0.4
    }
  }
}
```

`@density_function minecraft:overworld/caves/spaghetti_2d_thickness_modulator`

```json
{
  "type": "minecraft:cache_once",
  "argument": {
    "type": "minecraft:add",
    "argument1": -0.95,
    "argument2": {
      "type": "minecraft:mul",
      "argument1": -0.35000000000000003,
      "argument2": {
        "type": "minecraft:noise",
        "noise": "minecraft:spaghetti_2d_thickness",
        "xz_scale": 2,
        "y_scale": 1
      }
    }
  }
}
```

`@density_function minecraft:overworld/caves/spaghetti_2d`

```json
{
  "type": "minecraft:clamp",
  "input": {
    "type": "minecraft:max",
    "argument1": {
      "type": "minecraft:add",
      "argument1": {
        "type": "minecraft:weird_scaled_sampler",
        "input": {
          "type": "minecraft:noise",
          "noise": "minecraft:spaghetti_2d_modulator",
          "xz_scale": 2,
          "y_scale": 1
        },
        "noise": "minecraft:spaghetti_2d",
        "rarity_value_mapper": "type_2"
      },
      "argument2": {
        "type": "minecraft:mul",
        "argument1": 0.083,
        "argument2": "minecraft:overworld/caves/spaghetti_2d_thickness_modulator"
      }
    },
    "argument2": {
      "type": "minecraft:cube",
      "argument": {
        "type": "minecraft:add",
        "argument1": {
          "type": "minecraft:abs",
          "argument": {
            "type": "minecraft:add",
            "argument1": {
              "type": "minecraft:add",
              "argument1": 0.0,
              "argument2": {
                "type": "minecraft:mul",
                "argument1": 8.0,
                "argument2": {
                  "type": "minecraft:noise",
                  "noise": "minecraft:spaghetti_2d_elevation",
                  "xz_scale": 1,
                  "y_scale": 0
                }
              }
            },
            "argument2": {
              "type": "minecraft:y_clamped_gradient",
              "from_y": -64,
              "to_y": 320,
              "from_value": 8,
              "to_value": -40
            }
          }
        },
        "argument2": "minecraft:overworld/caves/spaghetti_2d_thickness_modulator"
      }
    }
  },
  "min": -1,
  "max": 1
}
```

`@density_function minecraft:overworld/caves/entrances`

```json
{
  "type": "minecraft:cache_once",
  "argument": {
    "type": "minecraft:min",
    "argument1": {
      "type": "minecraft:add",
      "argument1": {
        "type": "minecraft:noise",
        "noise": "minecraft:cave_entrance",
        "xz_scale": 0.75,
        "y_scale": 0.5
      },
      "argument2": {
        "type": "minecraft:add",
        "argument1": 0.37,
        "argument2": {
          "type": "minecraft:y_clamped_gradient",
          "from_y": -10,
          "to_y": 30,
          "from_value": 0.3,
          "to_value": 0
        }
      }
    },
    "argument2": {
      "type": "minecraft:add",
      "argument1": "minecraft:overworld/caves/spaghetti_roughness_function",
      "argument2": {
        "type": "minecraft:clamp",
        "input": {
          "type": "minecraft:add",
          "argument1": {
            "type": "minecraft:max",
            "argument1": {
              "type": "minecraft:weird_scaled_sampler",
              "input": {
                "type": "minecraft:cache_once",
                "argument": {
                  "type": "minecraft:noise",
                  "noise": "minecraft:spaghetti_3d_rarity",
                  "xz_scale": 2,
                  "y_scale": 1
                }
              },
              "noise": "minecraft:spaghetti_3d_1",
              "rarity_value_mapper": "type_1"
            },
            "argument2": {
              "type": "minecraft:weird_scaled_sampler",
              "input": {
                "type": "minecraft:cache_once",
                "argument": {
                  "type": "minecraft:noise",
                  "noise": "minecraft:spaghetti_3d_rarity",
                  "xz_scale": 2,
                  "y_scale": 1
                }
              },
              "noise": "minecraft:spaghetti_3d_2",
              "rarity_value_mapper": "type_1"
            }
          },
          "argument2": {
            "type": "minecraft:add",
            "argument1": -0.0765,
            "argument2": {
              "type": "minecraft:mul",
              "argument1": -0.011499999999999996,
              "argument2": {
                "type": "minecraft:noise",
                "noise": "minecraft:spaghetti_3d_thickness",
                "xz_scale": 1,
                "y_scale": 1
              }
            }
          }
        },
        "min": -1,
        "max": 1
      }
    }
  }
}
```

`@density_function minecraft:overworld/caves/noodle`

```json
{
  "type": "minecraft:range_choice",
  "input": {
    "type": "minecraft:interpolated",
    "argument": {
      "type": "minecraft:range_choice",
      "input": "minecraft:y",
      "min_inclusive": -60,
      "max_exclusive": 321,
      "when_in_range": {
        "type": "minecraft:noise",
        "noise": "minecraft:noodle",
        "xz_scale": 1,
        "y_scale": 1
      },
      "when_out_of_range": -1
    }
  },
  "min_inclusive": -1000000,
  "max_exclusive": 0,
  "when_in_range": 64,
  "when_out_of_range": {
    "type": "minecraft:add",
    "argument1": {
      "type": "minecraft:interpolated",
      "argument": {
        "type": "minecraft:range_choice",
        "input": "minecraft:y",
        "min_inclusive": -60,
        "max_exclusive": 321,
        "when_in_range": {
          "type": "minecraft:add",
          "argument1": -0.07500000000000001,
          "argument2": {
            "type": "minecraft:mul",
            "argument1": -0.025,
            "argument2": {
              "type": "minecraft:noise",
              "noise": "minecraft:noodle_thickness",
              "xz_scale": 1,
              "y_scale": 1
            }
          }
        },
        "when_out_of_range": 0
      }
    },
    "argument2": {
      "type": "minecraft:mul",
      "argument1": 1.5,
      "argument2": {
        "type": "minecraft:max",
        "argument1": {
          "type": "minecraft:abs",
          "argument": {
            "type": "minecraft:interpolated",
            "argument": {
              "type": "minecraft:range_choice",
              "input": "minecraft:y",
              "min_inclusive": -60,
              "max_exclusive": 321,
              "when_in_range": {
                "type": "minecraft:noise",
                "noise": "minecraft:noodle_ridge_a",
                "xz_scale": 2.6666666666666665,
                "y_scale": 2.6666666666666665
              },
              "when_out_of_range": 0
            }
          }
        },
        "argument2": {
          "type": "minecraft:abs",
          "argument": {
            "type": "minecraft:interpolated",
            "argument": {
              "type": "minecraft:range_choice",
              "input": "minecraft:y",
              "min_inclusive": -60,
              "max_exclusive": 321,
              "when_in_range": {
                "type": "minecraft:noise",
                "noise": "minecraft:noodle_ridge_b",
                "xz_scale": 2.6666666666666665,
                "y_scale": 2.6666666666666665
              },
              "when_out_of_range": 0
            }
          }
        }
      }
    }
  }
}
```

`@density_function minecraft:overworld/caves/pillars`

```json
{
  "type": "minecraft:cache_once",
  "argument": {
    "type": "minecraft:mul",
    "argument1": {
      "type": "minecraft:add",
      "argument1": {
        "type": "minecraft:mul",
        "argument1": {
          "type": "minecraft:noise",
          "noise": "minecraft:pillar",
          "xz_scale": 25,
          "y_scale": 0.3
        },
        "argument2": 2
      },
      "argument2": {
        "type": "minecraft:add",
        "argument1": -1.0,
        "argument2": {
          "type": "minecraft:mul",
          "argument1": -1.0,
          "argument2": {
            "type": "minecraft:noise",
            "noise": "minecraft:pillar_rareness",
            "xz_scale": 1,
            "y_scale": 1
          }
        }
      }
    },
    "argument2": {
      "type": "minecraft:cube",
      "argument": {
        "type": "minecraft:add",
        "argument1": -1.0,
        "argument2": {
          "type": "minecraft:mul",
          "argument1": -1.0,
          "argument2": {
            "type": "minecraft:noise",
            "noise": "minecraft:pillar_thickness",
            "xz_scale": 1,
            "y_scale": 1
          }
        }
      }
    }
  }
}
```
