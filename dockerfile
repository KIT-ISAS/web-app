FROM python:3.10.12 AS base

WORKDIR /code

RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock /code/
RUN poetry sync --no-root --without dev

COPY ./app.py /code/app.py
COPY ./assets /code/assets
COPY ./pages  /code/pages
COPY ./util /code/util
COPY ./components /code/components
COPY ./renderer /code/renderer
COPY ./model /code/model


FROM base AS tests
RUN apt-get update && apt-get install -y chromium chromium-driver
RUN poetry sync --no-root --with dev
COPY ./tests /code/tests
CMD ["poetry", "run", "pytest", "--headless"]

FROM base AS prod
CMD ["poetry", "run", "gunicorn", "--workers", "1", "--bind", "0.0.0.0:8080", "app:server"]
