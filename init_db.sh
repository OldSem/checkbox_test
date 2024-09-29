#!/bin/bash
set -e

# Создаем вторую базу данных
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER"  $POSTGRES_DB<<-EOSQL
    CREATE DATABASE test;
EOSQL