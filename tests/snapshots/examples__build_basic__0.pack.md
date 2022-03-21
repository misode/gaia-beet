# Lectern snapshot

## Data pack

`@data_pack pack.mcmeta`

```json
{
  "pack": {
    "pack_format": 9,
    "description": ""
  }
}
```

### basic

`@density_function basic:foo`

```json
{
  "type": "minecraft:add",
  "argument1": {
    "type": "minecraft:abs",
    "argument": {
      "type": "minecraft:cube",
      "argument": 4
    }
  },
  "argument2": {
    "type": "minecraft:slide",
    "argument": 2
  }
}
```

`@density_function basic:bar`

```json
{
  "type": "minecraft:mul",
  "argument1": {
    "type": "minecraft:slide",
    "argument": 2
  },
  "argument2": "basic:foo"
}
```

`@density_function basic:baz`

```json
{
  "type": "minecraft:min",
  "argument1": 1,
  "argument2": {
    "type": "minecraft:min",
    "argument1": 2,
    "argument2": 3
  }
}
```
