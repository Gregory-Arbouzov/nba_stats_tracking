import psycopg2
from psycopg2.extensions import register_adapter, AsIs

import numpy as np

from .config import *

register_adapter(np.int64, AsIs)

postgres_config = DatabaseConfig(filename = 'database.ini', section = 'postgresql')

class CreateSqlTables:
    def __init__(self, file, config):
        self.connection = None
        self.file = file
        self.config = config

    try:
        params = self.config

        print('connecting to postgresql database...')
        connection = psycopg2.connect(**params)

        print("connection successful / task complete")
       
        # create cursor
        cursor = connection.cursor()

        
        # add all sql create table commands here
        #cursor.execute(open('create_game_results_table.sql', 'r').read())
        #cursor.execute(open('create_yearly_team_per_game_stats_table.sql', 'r').read())
        #cursor.execute(open('create_yearly_opponent_per_game_stats_table.sql', 'r').read())

        try:
            
            # add all sql create table commands here
            #cursor.execute(open('create_game_results_table.sql', 'r').read())
            #cursor.execute(open('create_yearly_team_per_game_stats_table.sql', 'r').read())
            #cursor.execute(open('create_yearly_opponent_per_game_stats_table.sql', 'r').read())


            connection.commit()
            print("connection successful / task complete")
            cursor.close()
            #os.remove(tmp_df)
            
        except (Exception, psycopg2.DatabaseError) as error:
            #os.remove(tmp_df)
            print("Error: %s" % error)
            #connection.rollback()
            cursor.close()
    
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if connection is not None:
            connection.close()
            print('database connection terminated')
