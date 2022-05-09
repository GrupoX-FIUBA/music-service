import os

DATABASE_URL = os.environ["DATABASE_URL"].replace("postgres://",
                                                  "postgresql://", 1)
