# gaia-beet

[![GitHub Actions](https://github.com/misode/gaia/workflows/CI/badge.svg)](https://github.com/misode/gaia-beet/actions)
[![PyPI](https://img.shields.io/pypi/v/gaia-beet.svg)](https://pypi.org/project/gaia-beet/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gaia-beet.svg)](https://pypi.org/project/gaia-beet/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Discord](https://img.shields.io/discord/900530660677156924?color=7289DA&label=discord&logo=discord&logoColor=fff)](https://discord.gg/98MdSGMm8j)

> Beet plugin to generate Minecraft worldgen files

## Introduction

Writing density functions in JSON by hand can be tiring and confusing. This package allows you to write them as natural looking expressions.

```py
gaia.df("basic:foo", abs(const(4) ** 3) + ref("basic:bar"))
```

## Installation

The package can be installed with `pip`.

```bash
$ pip install gaia-beet
```

## Getting started

When using with [`beet`](https://github.com/mcbeet/beet), a simple `beet.yml` is enough:
```yml
pipeline:
  - main
```

This references a `main.py` plugin file where the density functions will be defined:
```py
from beet import Context
from gaia_beet import Gaia
from gaia_beet.density_functions import *

def beet_default(ctx: Context):
    gaia = ctx.inject(Gaia)

    blah = slide(const(2))

    foo = gaia.df("basic:foo", abs(const(4) ** 3) + blah)

    gaia.df("basic:bar", blah * foo)
```

## Contributing

Contributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org).

```bash
$ poetry install
```

You can run the tests with `poetry run pytest`.

```bash
$ poetry run pytest
```

The project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you're using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically. You can also install the type-checker locally with `npm install` and run it from the command-line.

```bash
$ npm run watch
$ npm run check
```

The code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).

```bash
$ poetry run isort gaia_beet examples tests
$ poetry run black gaia_beet examples tests
$ poetry run black --check gaia_beet examples tests
```

---

License - [MIT](https://github.com/misode/gaia-beet/blob/main/LICENSE)
