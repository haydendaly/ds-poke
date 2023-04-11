# DS in the Wild Project: Pokemon Card Identification

[Initial Proposal: Google Slides](https://docs.google.com/presentation/d/1t7WQ5hytdsKvZk0Yyzdm0pFz0CW3NU4ZImZ9vTHxLuE/edit?usp=sharing)

## Setup

```sh
$ curl -sSL https://install.python-poetry.org | python3 -
$ poetry install
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

### Data Scraping (WIP)

This spins up an async worker queue and writes images to an SSD.

```sh
$ poetry run cgc
```

## Directory Hierarchy

The project is broken into different modules which export the methods / variables specified in the respective `__init__.py` files.

```sh
src
├── classification
│   └── __init__.py
├── dataset
│   ├── __init__.py
│   └── cgc.py # pandas DataFrame for CGC data
├── image
│   ├── __init__.py
│   ├── helpers
│   │   ├── __init__.py
│   │   ├── color.py
│   │   ├── compare.py
│   │   ├── crop.py
│   │   └── display.py
│   └── storage.py # CDN-esque interface for local storage
├── main.ipynb
├── scrape # data scraping scripts
│   ├── __init__.py
│   ├── browser.py
│   └── source
│       ├── __init__.py
│       └── cgc
│           ├── __init__.py
│           ├── label_classifier.py # simple classifier for data cleaning
│           └── scraper.py
├── scripts # scripts for `poetry run [cmd]` commands
│   ├── lint.py
│   ├── notebook.py
│   └── precommit.py
├── segmentation
│   └── __init__.py
└── shared
    ├── __init__.py
    ├── constant.py
    ├── error.py
    └── json.py
```
