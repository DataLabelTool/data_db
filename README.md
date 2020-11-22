# data_db

MongoDB for hierarchical_label_tool

## Setup

Edit `.env` file at `docker/.env` catalog with your values:

```
COMPOSE_PROJECT_NAME=data_db
MONGO_ROOT_USER=devroot
MONGO_ROOT_PASSWORD=devroot
MONGO_PORT=27017
MONGOEXPRESS_LOGIN=dev
MONGOEXPRESS_PASSWORD=dev
MONGOEXPRESS_PORT=8081
```

## Run

```bash
cd docker
docker-compose up -d
```

## todo:

- создание первого пользователя админа