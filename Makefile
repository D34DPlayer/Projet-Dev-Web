include .env

compose_file ?= "docker-compose.yml"
project ?= "devweb"

DC = docker-compose -p $(project) -f $(compose_file)

password ?= superpassword
hashed_password ?= ` \
	$(DC) exec api   \
		python -c "from passlib.context import CryptContext;print(CryptContext(schemes=['bcrypt'], deprecated='auto').hash('$(password)'))"`

define HELP
Utilitaire docker-compose

Commandes:
----------
    build    - Build le docker-compose.
    start    - Démarre les containers. Alias: up
    stop     - Arrête les containers. Alias: down
    restart  - Redémarre les containers.
    upgrade  - Met à jour la base de données.
    revision - Crée une révision de la base de donnée. Alias: rev
    setup_db - Setup la base de donnée.
               Pour changer le mot de passe par défaut du compte admin:
                  `make setup_db password=motdepasse`
    help     - Affiche l'aide.
endef
export HELP

help:
	@echo "$$HELP"

build:
	$(DC) build

start up:
	$(DC) up -d

stop down:
	$(DC) down

restart:
	$(DC) restart

upgrade: start
	$(DC) exec --workdir /api api alembic upgrade head

revision rev: start
	@read -p "Revision name: " rev; \
	$(DC) exec --workdir /api api alembic revision --autogenerate -m "$(rev)"

setup_db: upgrade
	@$(DC) exec db psql $(DB_NAME) $(DB_USER) -c "  \
		INSERT INTO                                 \
			users(username, email, hashed_password) \
		VALUES(                                     \
			'admin',                                \
			'admin@boucherie.tk',                   \
			'$(hashed_password)'                    \
		);"

	@echo User: admin
	@echo Password: $(password)
