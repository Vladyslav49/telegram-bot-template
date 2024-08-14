# 🌟 Telegram Bot Template

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Python](https://img.shields.io/badge/python-3.12.5-blue)](https://www.python.org/downloads)
[![codecov](https://codecov.io/gh/Vladyslav49/telegram-bot-template/branch/develop/graph/badge.svg?token=2VLCKDIN0B)](https://codecov.io/gh/Vladyslav49/telegram-bot-template)

## 🛠️ Tech Stack

- [`aiogram`](https://github.com/aiogram/aiogram)
- [`aiogram-dialog`](https://github.com/Tishka17/aiogram_dialog)
- [`aiogram-i18n`](https://github.com/aiogram/i18n)
- [`aiogram-broadcaster`](https://github.com/loRes228/aiogram_broadcaster)
- [`sqlalchemy`](https://github.com/sqlalchemy/sqlalchemy)
- [`alembic`](https://github.com/sqlalchemy/alembic)
- [`dishka`](https://github.com/reagento/dishka)

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/Vladyslav49/telegram-bot-template
   ```

2. Navigate to the project directory:
   ```bash
   cd telegram-bot-template
   ```

3. Copy the configuration file and change the `TELEGRAM_BOT_API_TOKEN` variable to your token:
   ```bash
   cp .env.example .env
   ```

4. Start the Docker containers:
   ```bash
   docker compose -f compose.yaml up --build
   ```
