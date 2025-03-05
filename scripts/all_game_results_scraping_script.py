from scraping.helpers import *
from db.config import DatabaseConfig
from db.all_db_stuff import *
from db.sql_queries import *

import psycopg2
from configparser import ConfigParser

#db.connect.DatabaseConfig(filename = 'database.ini', section = 'postgresql')

postgres_config = DatabaseConfig(filename = 'db/database.ini', section = 'postgresql')
    
db1 = Database(postgres_config.get_config_params())
db1.connect()
#print(db1.get_data(sql_queries.get_all_game_results_dates_already_in_db))
#db1.create_table('db/create_table_files/create_game_dates_already_scraped_table.sql')

db1.close()


