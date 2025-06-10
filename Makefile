.PHONY: build up down logs

build:
	DOCKER_BUILDKIT=1 docker compose -f deploy/docker-compose.prod.yaml build

up: build
	docker compose -f deploy/docker-compose.prod.yaml up -d

down:
	docker compose -f deploy/docker-compose.prod.yaml down

logs:
	docker compose -f deploy/docker-compose.prod.yaml logs -f