class Config(object):
    POSTS_PER_PAGE = 10


class ProdConfig(Config):
    pass


class DevConfig(Config):
    debug = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# mysql+pymysql://root@localhost/jafary
# 
