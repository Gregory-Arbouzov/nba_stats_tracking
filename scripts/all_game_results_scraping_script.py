# make sure export pythonpath does not double reference the same path ie user/garbouzov....user/garbouzov
# use export PYTHONPATH=../nba_stats_tracking 

from scraping import helpers, daily_game_scrape
from db import config, all_db_stuff, sql_queries

import psycopg2
from configparser import ConfigParser

valid_game_days = helpers.valid_game_days

postgres_config = config.DatabaseConfig(filename = 'db/database.ini', section = 'postgresql')
    
db1 = all_db_stuff.Database(postgres_config.get_config_params())
db1.connect()

days_with_results_raw = db1.get_data(sql_queries.get_all_game_results_dates_already_in_db)
days_with_results = [x[0] for x in days_with_results_raw]

days_with_scrape_attempts_raw = db1.get_data(sql_queries.get_all_scrape_attempt_dates)
days_with_scrape_attempts = [x[0] for x in days_with_scrape_attempts_raw]

for day in valid_game_days:
    if day in days_with_scrape_attempts:
        print('day has already been scraped ' + str(day))
    elif day in days_with_results:
        try:
            print('day already has game results ' + str(day))
            db1.insert_data("""INSERT INTO game_dates_already_scraped (id, dates) VALUES (%s, %s); """, (day, day))
        except psycopg2.Error as error:
            print('Failed to insert data into scrape attempts table:', error)
    else:
        try:
            db1.insert_data("""INSERT INTO game_dates_already_scraped (id, dates) VALUES (%s, %s); """, (day, day))
            day_game_data = daily_game_scrape.GameResults(str(day)).get_results(api_connection = True)

            for index in day_game_data.index:
                db1.insert_data("""INSERT INTO game_results (id, visitor, home, dates, visitor_score, home_score) VALUES (%s, %s, %s, %s, %s, %s); """, tuple(day_game_data.iloc[index]))
            print('Finished inserting game result data for ' + str(day))
        except psycopg2.Error as error:
            print('Failed to insert data into game results table:', error)

db1.close()


