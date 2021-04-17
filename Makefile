include .env
DC = docker-compose -p devweb

password ?= superpassword
hashed_password ?= ` \
	$(DC) exec api   \
		python -c "from passlib.context import CryptContext;print(CryptContext(schemes=['bcrypt'], deprecated='auto').hash('$(password)'))"`

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
