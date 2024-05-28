.PHONY: help

help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build docker image
	@docker build -t prometheus-container-exporter:build -f docker/Dockerfile.build . && \
	docker compose -f docker-compose.yml build

## production

start: ## Start container exporter service
	@docker compose -f docker-compose.yml up -d

stop: ## Stop container exporter service
	@docker compose -f docker-compose.yml down --remove-orphans

## Dev

dev: ## Dev in container
	@docker build -t prometheus-container-exporter:build -f docker/Dockerfile.build . && \
	docker compose -f docker-compose.dev.yml build && \
	docker compose -f docker-compose.dev.yml up

clean: ## Clean dev containers
	docker compose -f docker-compose.dev.yml down
