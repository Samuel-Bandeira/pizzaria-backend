# Commit Migration:

poetry run alembic revision --autogenerate -m "comment"

# Run Migration:

poetry run alembic upgrade head
