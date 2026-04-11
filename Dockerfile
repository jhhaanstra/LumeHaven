FROM python:3.14.4-alpine

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /bin/

# Copy requires resources
COPY ./src /lumehaven/src
COPY ./uv.lock /lumehaven
COPY ./pyproject.toml /lumehaven
COPY ./README.md /lumehaven

# Disable development dependencies
ENV UV_NO_DEV=1

WORKDIR /lumehaven
RUN uv sync --locked

CMD ["uv", "run", "lumehaven"]