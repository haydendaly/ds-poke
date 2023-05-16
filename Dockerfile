FROM python:3.9

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-dev

COPY . .

ARG ENTRYPOINT_MODULE
ENTRYPOINT ["python", "-m", "${ENTRYPOINT_MODULE}"]
