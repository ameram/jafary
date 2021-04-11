class Config(object):
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    debug = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/jafary"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
