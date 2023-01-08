# Python Client for the Upsilon Workshop

## Development environment setup

To install the API, you need to have a working installation of Python 3.10 or
higher. You also need to have a working installation of pip.

### Virtualenv (optional)

It is recommended to use a virtualenv to install the API. This will allow you
to install the API without affecting your system's Python installation.

To create a virtualenv, run:

```bash
pip install virtualenv
virtualenv env
```

To activate the virtualenv, run:

```bash
source env/bin/activate
```

### Dependencies

We use [Poetry](https://python-poetry.org/) to manage dependencies. To install
Poetry, run:

```bash
pip install poetry
```

To install the dependencies, run:

```bash
poetry install
```

