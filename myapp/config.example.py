#coding: utf-8
import string
import weibo
from weibo import *
import sys
from sqlalchemy.pool import NullPool 

reload(sys)
sys.setdefaultencoding('utf8') 

if 'SERVER_SOFTWARE' in os.environ:

    SAE_MYSQL_HOST_M = 'w.rdc.sae.sina.com.cn'
    SAE_MYSQL_HOST_S = 'r.rdc.sae.sina.com.cn'
    SAE_MYSQL_PORT = '3307'

    APP_KEY = ''
    APP_SECRET = ''
    CALLBACK_URL = ''

    mysql_db = 'app_%s' % ''
    mysql_user = APP_KEY
    mysql_pass = APP_SECRET

    DATABASE_USER = sae.const.MYSQL_USER
    DATABASE_PWD =sae.const.MYSQL_PASS
    DATABASE_NAME= sae.const.MYSQL_DB
    DATABASE_HOST=sae.const.MYSQL_HOST
    DATABASE_PORT=sae.const.MYSQL_PORT
    DB = create_engine('mysql://%s:%s@%s:%s/%s'% (DATABASE_USER,DATABASE_PWD,DATABASE_HOST,DATABASE_PORT,DATABASE_NAME),connect_args={'charset':'utf8'},echo=False,poolclass=NullPool)
    Base = declarative_base()

else:
    APP_KEY = ''
    APP_SECRET = ''
    CALLBACK_URL = 'http://127.0.0.1:5000/oauth'

    DATABASE_USER = 'root'
    DATABASE_PWD =''
    DATABASE_NAME= 'whyfans'
    DATABASE_HOST='127.0.0.1'
    DATABASE_PORT='3306'
    DB = create_engine('mysql://%s:%s@%s:%s/%s'% (DATABASE_USER,DATABASE_PWD,DATABASE_HOST,DATABASE_PORT,DATABASE_NAME),connect_args={'charset':'utf8'},echo=True,poolclass=NullPool)

db_session=sessionmaker(bind=DB)
dbSession=db_session()