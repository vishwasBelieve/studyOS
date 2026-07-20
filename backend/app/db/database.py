from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg://studyos_admin:studyos_db:220pc@localhost:5432/studyos_db"

engine = create_engine(DATABASE_URL)
print(engine)
print(type(engine))