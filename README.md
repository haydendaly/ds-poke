# DS in the Wild Project: Pokemon Card Identification

[Initial Proposal: Google Slides](https://docs.google.com/presentation/d/1t7WQ5hytdsKvZk0Yyzdm0pFz0CW3NU4ZImZ9vTHxLuE/edit?usp=sharing)

## Setup

```sh
$ curl -sSL https://install.python-poetry.org | python3 -
$ poetry install
$ poetry run setup
```

To add packages, you can use:

```sh
$ poetry add <package-name>
```

## Usage

### Jupyter

You can start a Jupyter notebook server with:

```sh
$ poetry run notebook
```

This will add the `Pokemon Identification` kernel to Jupyter and open up `localhost:8888` for Jupyter hub. As a result, you will be able to access the up-to-date dependencies and local modules.

This will run in its own terminal and you can `CTRL-C` it to stop the server.

### Lint

```sh
$ poetry run lint
```

### Test

```sh
$ poetry run pytest
```

### CGC Data Scraping (WIP)

This spins up an async worker queue and writes images to an SSD.

```sh
$ poetry run cgc
```

## Directory Hierarchy

The project is broken into different modules which export the methods / variables specified in the respective `__init__.py` files.

```sh
src
├── classification
│   ├── __init__.py
│   └── cgc_label_classifier.py
├── dataset
│   ├── __init__.py
│   └── cgc.py
├── image
│   ├── __init__.py
│   ├── helpers.py
│   └── storage.py
├── main.ipynb
├── scrape
│   ├── __init__.py
│   ├── browser.py
│   └── cgc.py
├── scripts.py
├── segmentation
│   └── __init__.py
└── shared
    ├── __init__.py
    ├── constant.py
    ├── error.py
    ├── json.py
    └── warning.py
```
