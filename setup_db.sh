docker-compose -p devweb run api alembic upgrade head

docker-compose -p devweb run db psql -U postgres -c "INSERT INTO users (username, email, hashed_password) VALUES ('admin', 'admin@boucherie.tk', '$2b$12$FmDCDxROtlOb8vNdYSf0nOcoKv67ez1q2w4mWC.DeOSnm5JwpdpbW');"

echo "User: admin\nPwd: superpassword"
