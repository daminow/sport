###############################################################################
#  sportsite-dev.sh  —  “одна кнопка” для работы с проектом sportSite
#  Сохраните файл, например, в  ~/sportSite/scripts/sportsite-dev.sh
#  и добавьте строку  source ~/sportSite/scripts/sportsite-dev.sh  в ~/.bashrc
#
#  После этого команда  sport  <subcommand>  будет управлять стеком:
#      sport pull        — git pull
#      sport up          — пересборка + запуск (без очистки кэша)
#      sport restart     — мягкий рестарт backend-контейнера
#      sport build       — rebuild adminpanel (кэш слоёв сохранён)
#      sport test        — pytest
#      sport lint        — ruff check .
#      sport logs        — live-логи Django
#      sport status      — docker compose ps
#      sport exec CMD    — выполнить CMD внутри adminpanel
#      sport clean       — полная остановка + prune (освобождает место)
###############################################################################

# где лежит репозиторий
export SPORT_ROOT="${SPORT_ROOT:-$HOME/sportSite}"
# чтобы не писать каждый раз -f deploy/docker-compose.yaml
export COMPOSE_FILE="$SPORT_ROOT/deploy/docker-compose.yaml"

sport() {
    cd "$SPORT_ROOT" || { echo "✗ no $SPORT_ROOT"; return 1; }

    case "$1" in
        pull)      git pull ;;
        up)        docker compose up --build -d ;;
        restart)   docker compose restart adminpanel ;;
        build)     docker compose build adminpanel && docker compose up -d adminpanel ;;
        status)    docker compose ps ;;
        logs)      docker compose logs -f adminpanel ;;
        test)      docker compose exec adminpanel poetry run pytest -q ;;
        lint)      docker compose exec adminpanel poetry run ruff check . ;;
        exec)      shift; docker compose exec adminpanel "$@" ;;
        clean)     docker compose down && \
                   docker system prune -af && docker volume prune -f ;;
        help|"")   cat <<EOF
Usage: sport <command>

  pull        git pull
  up          build & start all containers
  restart     restart only adminpanel
  build       rebuild adminpanel image (deps cache retained)
  status      docker compose ps
  logs        live logs of adminpanel
  test        run pytest
  lint        run ruff
  exec CMD    run arbitrary CMD inside adminpanel
  clean       stop stack and prune docker cache
EOF
                   ;;
        *)        echo "Unknown command: $1 (try 'sport help')" ;;
    esac
}