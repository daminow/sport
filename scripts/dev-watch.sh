#!/usr/bin/env bash
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"            # теперь мы гарантированно в /root/sportSite

while inotifywait -r -e modify,create,delete,move \
        --exclude '/(\.git|__pycache__|\.venv)/' \
        adminpage deploy scripts; do

    echo -e "\n⚙️  Изменения найдены — пересобираю контейнеры..."
    docker compose -f deploy/docker-compose.yaml up --build -d

    echo "🧪  Запускаю тесты и линтеры..."
    docker compose exec adminpanel poetry run pytest -q
    docker compose exec adminpanel poetry run ruff check .
    echo -e "✅  Готово — жду следующих изменений.\n"
done