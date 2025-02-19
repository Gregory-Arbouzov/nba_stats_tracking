from db import config
from db import all_db_stuff

import psycopg2
from configparser import ConfigParser

#db.connect.DatabaseConfig(filename = 'database.ini', section = 'postgresql')

postgres_config = config.DatabaseConfig(filename = 'db/database.ini', section = 'postgresql')
    
db1 = all_db_stuff.Database(postgres_config.get_config_params())
db1.connect()

db1.close()
