# Visualization Pipeline

## Installation

To install the official PyPI release, simply run `pip install vispipe`. To install from source, clone the repo into a directory and then run: 

```
uv venv
.venv\Scripts\activate
uv pip install .
```

## Examples
There is a very basic example in the example/ dir. Included are sample data files, a `config.json`, and a copy of `settings.json` already installed in the package. To set up the example, run:

```powershell
cd example/
uv venv
.venv\Scripts\activate
uv pip install ../ .
```

This will install the necessary readers for the data files. From there, the `config.json` and `settings.json` can be edited and used.

## Documentation
Documentation can be found on [readthedocs.io](https://vispipe.readthedocs.io/en/latest/). Included in this repo are the Sphinx source files for the documentation. To build, run the following commands:

```
cd src/docs
uv venv
.venv\Scripts\activate
uv pip install ../../ -r requirements.txt
sphinx-build -M html ./source ./build
```

The HTML files will be generated and the homepage will be located at `vispipe\src\docs\build\html\index.html`.
