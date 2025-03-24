FROM python:3.12.7

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0

RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app/src:${PYTHONPATH}" 

COPY ./src/pyproject.toml ./src/poetry.lock /app/src/

WORKDIR /app/src/
RUN poetry install --no-root

COPY ./src/facehunter/ /app/src/facehunter/

WORKDIR /app/src/facehunter/
