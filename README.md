# Flask Shop - Docker Compose Practice

A complete practice project with a working frontend and backend.

## Stack

- HTML/CSS frontend
- Flask backend
- MySQL database
- Dockerfile
- Docker Compose
- MySQL named volume
- init.sql database initialization
- No .env file

## Structure

flask-compose-shop-full/
├── app.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── init.sql
├── templates/
│   └── index.html
└── static/
    └── style.css

## Run

From this folder:

    docker compose up --build

Or background:

    docker compose up --build -d

Open:

    http://localhost:5000

You can:
- view products
- add products
- delete products
- check database health

## Useful commands

    docker compose ps
    docker compose logs -f
    docker compose logs -f flask
    docker compose logs -f mysql
    docker compose exec flask sh

Stop:

    docker compose down

Stop and remove this project's database volume:

    docker compose down -v

WARNING: `down -v` deletes the MySQL data for this project.

## Important

This project intentionally has NO `.env` file.
Environment variables are directly inside compose.yaml for learning.

MySQL is also inside Docker, so this project does not use the MySQL server
already installed on Ubuntu.

The first MySQL startup runs init.sql. If the mysql-data volume already exists,
MySQL initialization scripts will not run again.
