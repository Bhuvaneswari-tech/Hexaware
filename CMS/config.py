import os

class Config:
    # MySQL connection string
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/elearning"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
