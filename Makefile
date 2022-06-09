.PHONY: build, shell

build:
	@.scripts/docker_build.sh

shell:
	@docker compose run shell
