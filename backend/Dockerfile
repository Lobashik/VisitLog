FROM python:3.12.7

RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app/src" 

COPY ./src/pyproject.toml ./src/poetry.lock /app/src/

WORKDIR /app/src/
RUN poetry install --no-root

COPY ./src/cameras/ /app/src/cameras/

WORKDIR /app/src/cameras/
