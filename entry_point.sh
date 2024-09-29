#!/bin/bash



./wait-for-it.sh local_db:5432 -- alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000
