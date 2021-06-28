class Config(object):
    POSTS_PER_PAGE = 10
    SECRET_KEY ='\xb2\x0c\xe2\xb4SQ\xcb\xaad\xe6H\xaf\xf2\xbc\xa3\xad\xa0tbQQ\xfc\xce\xde'


class ProdConfig(Config):
    SECRET_KEY = 'w\x1a"o\xeb\xa6: c\xc0\x95j\x1f\xceW\xfbs7 %\xbb\x9dvQ\x94y'


class DevConfig(Config):
    debug = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@127.0.0.1/moshavere"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "\x02\xd0\xbf'\xfc\xdc\xfaV\x97\xb6\x06\xa9\\g\xf2\xe8\xa4\xd5\xc1\xce\xdd\xefa\x0c"

# 
#  "sqlite:///database.db"
