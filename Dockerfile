# Base Image
FROM python:3.11.9-alpine as base
# Print to stdout without buffering
ENV PYTHONUNBUFFERED=1
# Don't generate *.pyc files
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
ENV PYTHONPATH="./"


FROM base as builder
USER root
# Install build dependencies
ARG BUILD_DEPS="gcc \
                musl-dev \
                libffi-dev \
                curl"
RUN apk add --update --no-cache ${BUILD_DEPS} --repository=https://dl-cdn.alpinelinux.org/alpine/edge/main/
# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3
ENV PATH="${PATH}:/root/.local/bin"
# Set Poetry to create virtualenv in the project
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
# Install python packages by poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main


FROM base as runtime
USER root
# Copy the virtual environment from the builder stage
ENV VIRTUAL_ENV=/app/.venv
COPY --from=builder "$VIRTUAL_ENV" "$VIRTUAL_ENV"
# Activate the virtual environment
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY ./app ./
CMD ["python", "main.py"]