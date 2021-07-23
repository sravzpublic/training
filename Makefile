# This line is added in THIS version.
.PHONY: .EXPORT_ALL_VARIABLES

.EXPORT_ALL_VARIABLES:
# Update
SRAVZ_REPO_LOCATION=$(PWD)

# Docker image versions
export SRAVZ_TRAINING_VERSION=v1

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

print-env: ## Print Env
	env

docker-use-default-context: ## Docker use default context
	docker context use default

### Build Commands
docker-build: docker-use-default-context ## Builds docker image
	docker build --tag public.ecr.aws/b8h3z2a1/sravz/training:$(SRAVZ_TRAINING_VERSION) .

### Docker Push Image
docker-push: docker-use-default-context ## Docker: push docker images
	docker push public.ecr.aws/b8h3z2a1/sravz/training:$(SRAVZ_TRAINING_VERSION)

### Docker compose commands
docker-compose-rebuild-service: docker-use-default-context ## Rebuild docker compose service: make docker-compose-rebuild-service service=training
	docker-compose up -d --no-deps --build $(service)

docker-compose: docker-use-default-context## Run docker compose action: make docker-compose action=up/down
	docker network create training | true
	echo "Running docker command $(action)"; \
	if [ "$(action)" == "up" ]; then \
        docker compose $(action) -d; \
	else \
        docker compose $(action); \
	fi

docker-compose-tail-logs: docker-use-default-context ## Tails docker logs: make docker-compose-tail-logs service=training
	docker-compose logs -f --tail=10 $(service)

docker-exec: ## Exec into a docker container: make docker-exec service=training
	docker exec -it `docker ps -aqf "name=training_$(service)_1"` sh
