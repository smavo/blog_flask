
SQLITE = "sqlite:///project.db"
POSTGRESQL = "postgresql+psycopg2://postgres:1nd1.sm4rt%%@localhost:5432/blog_flask"


class Config:
    DEBUG = True
    SECRET_KEY = 'smavodev'

    SQLALCHEMY_DATABASE_URI = POSTGRESQL
