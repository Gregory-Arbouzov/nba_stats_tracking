from scraping import helpers
from db import config, all_db_stuff, sql_queries

import psycopg2
from configparser import ConfigParser

valid_game_days = helpers.valid_game_days

postgres_config = config.DatabaseConfig(filename = 'nba_stats_tracking/db/database.ini', section = 'postgresql')
    
db1 = all_db_stuff.Database(postgres_config.get_config_params())
db1.connect()

days_with_results_raw = db1.get_data(sql_queries.get_all_game_results_dates_already_in_db)
days_with_results = [x[0] for x in days_with_results_raw]

#print(days_with_results)

for day in valid_game_days[:100]:
    if day in days_with_results:
        try:
            print('attempting to insert ' + str(day))
            print("""INSERT INTO game_dates_already_scraped (id, dates) VALUES ({0}, {1}); """.format(tuple([day, day])))
            #db1.insert_data(("""INSERT INTO game_dates_already_scraped (id, dates) VALUES (%d, %d); """, (day, day)))
        except psycopg2.Error as error:
            print('Failed to insert data:', error)
    else:
        print(str(day) + ' has no data')

print(db1.get_data(sql_queries.get_all_scrape_attempt_dates))

db1.close()


