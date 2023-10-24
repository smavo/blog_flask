
import os
from dotenv import load_dotenv


load_dotenv()

SQLITE = os.getenv('SQLITE')


class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRESQL')
    CKEDITOR_PKG_TYPE = os.getenv('CKEDITOR_PKG_TYPE')
