FROM python:3.12.5-alpine AS dependencies

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml .

RUN python -m venv /opt/venv && \
    pip install --no-cache-dir uv~=0.2.36 && \
    uv pip install --requirement pyproject.toml --extra dev --no-cache

FROM python:3.12.5-alpine

ENV PATH="/opt/venv/bin:$PATH"

COPY --from=dependencies /opt/venv/ /opt/venv/

WORKDIR /app

COPY src src
COPY pyproject.toml config.toml logging_config.yaml alembic.ini README.md ./

RUN uv pip install -e . --no-deps --no-cache

ENTRYPOINT ["python", "-m"]
CMD ["telegram_bot_template.entry_points.bot"]
