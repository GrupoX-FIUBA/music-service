import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./db.sqlite3")\
                         .replace("postgres://", "postgresql://", 1)
