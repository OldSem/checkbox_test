create_env:
	cp ./config/docker/env ./config/docker/.env
	cp ./config/docker/env ./config/docker/venv.env

up:
	docker compose up --build

down:
	docker compose down

docker-clear:
	docker compose down -v

force_up:
	docker compose up --force-recreate

env_load:
	eval $(config/docker/env_load.sh config/docker/venv.env)

migrations:
	docker exec checkbox_fast_api alembic revision --autogenerate -m "Name migration"

test:
	docker exec  -it  checkbox_fast_api pytest
