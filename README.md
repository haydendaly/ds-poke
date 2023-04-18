# DS in the Wild Project: Pokemon Card Identification

[Initial Proposal: Google Slides](https://docs.google.com/presentation/d/1t7WQ5hytdsKvZk0Yyzdm0pFz0CW3NU4ZImZ9vTHxLuE/edit?usp=sharing)

## Setup

```sh
# Install Poetry
$ curl -sSL https://install.python-poetry.org | python3 -
# Install dependencies
$ poetry install
# Download datasets
$ poetry run setup
```

If setup fails, make sure you have accepted the invite to `haydendaly/ds-poke-shared` which contains a dataset.

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

### CGC Data Scraping

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
│   ├── cgc.py
│   ├── dataset.ipynb
│   ├── pokemontcg.py
│   ├── pokumon.py
│   └── segmentation.py
├── scrape
│   ├── __init__.py
│   ├── browser.py
│   ├── cgc.py
│   ├── pokumon.py
│   └── psa
│       ├── __init__.py
│       └── pop.py
├── scripts
│   ├── __init__.py
│   ├── archive
│   │   └── main.py
│   └── main.py
├── segmentation
│   ├── __init__.py
│   ├── classical_cv.ipynb
│   ├── segmentation.ipynb
│   └── segmentation_prepare_dataset.ipynb
└── shared
    ├── __init__.py
    ├── constant.py
    ├── error.py
    ├── file.py
    ├── image.py
    ├── json.py
    ├── log.py
    ├── storage
    │   ├── __init__.py
    │   ├── base.py
    │   ├── image.py
    │   └── json.py
    ├── time.py
    └── warning.py
```
