from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/pizzaria"

engine = create_engine(DATABASE_URL)
conn = engine.connect()
print("Conexão estabelecida com sucesso.")
