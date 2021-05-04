include .env

compose_file ?= "docker-compose.yml"
project ?= "devweb"

DC = docker-compose -p $(project) -f $(compose_file)

DC_test = docker-compose -p testdevweb -f docker-compose.test.yml

test_exit ?= 0

password ?= superpassword
hashed_password ?= `$(DC) exec -T api python -c "from passlib.context import CryptContext;print(CryptContext(schemes=['bcrypt'], deprecated='auto').hash('$(password)'), end='')"`

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

Tests:
------
    test-all        - Lance l'environnement de test et exécute les tests backend et frontend.
                      Pour que make s'arrête lorsqu'un test rate:
                        `make test-all test_exit=1`
    test-back       - Exécute que les tests unitaires backend.
    test-front-unit - Exécute que les tests unitaires frontend.
    test-front-e2e  - Exécute que les tests end-to-end frontend.
endef
export HELP

help:
	@echo "$$HELP"

build:
	$(DC) build

start up:
	$(DC) up -d

stop down:
	$(DC) down -t 3

restart:
	$(DC) restart

upgrade: start
	$(DC) exec -T --workdir /api api alembic upgrade head

revision rev: start
	@read -p "Revision name: " rev; \
	$(DC) exec --workdir /api api alembic revision --autogenerate -m "$$rev"

setup_db: upgrade
	@$(DC) exec -T db psql $(DB_NAME) $(DB_USER) -c "  \
		INSERT INTO                                 \
			users(username, email, hashed_password) \
		VALUES(                                     \
			'admin',                                \
			'admin@boucherie.tk',                   \
			'$(hashed_password)'                    \
		);"

	@echo User: admin
	@echo Password: $(password)

_test-setup:
	@echo Building the images...
	@$(DC_test) build
	@echo Setting up the test database...
	@$(DC_test) up -d db
	@sleep 3
	@$(DC_test) run -T --rm --workdir /api api alembic upgrade head

	@echo Adding the default user...
	-@$(DC_test) exec -T db psql test $(DB_USER) -c "                           \
		INSERT INTO                                                             \
			users(username, email, hashed_password)                             \
		VALUES(                                                                 \
			'admin',                                                            \
			'admin@boucherie.tk',                                               \
			'$$2b$$12$$uqs4lIt2y4etQje8zJeKBuV32nyXflM7vxovtlm2dXuLba8f8ySua'   \
		);"

_test-cleanup:
	@echo Deleting the test database...
	@$(DC_test) down
	@docker volume rm testdevweb_postgres_data

_test-back:
	@echo Running backend tests...
ifeq ($(test_exit),1)
	$(DC_test) run --rm api
else
	-$(DC_test) run --rm api
endif

test-front-unit:
	@echo Running frontend unit tests...
ifeq ($(test_exit),1)
	$(DC_test) run --rm web-unit
else
	-$(DC_test) run --rm web-unit
endif

_test-front-e2e:
	@echo Running frontend e2e tests...
ifeq ($(test_exit),1)
	$(DC_test) run --rm web-e2e
else
	-$(DC_test) run --rm web-e2e
endif

test-all: _test-setup _test-back test-front-unit _test-cleanup

test-back: _test-setup _test-back _test-cleanup

test-front-e2e: _test-setup _test-front-e2e _test-cleanup
