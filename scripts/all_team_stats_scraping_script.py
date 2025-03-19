from scraping import helpers, yearly_team_stats_scrape
from db import config, all_db_stuff, sql_queries

import psycopg2
from configparser import ConfigParser

postgres_config = config.DatabaseConfig(filename = 'db/database.ini', section = 'postgresql')
    
db1 = all_db_stuff.Database(postgres_config.get_config_params())
db1.connect()

team_seasons_with_results_raw = db1.get_data(sql_queries.get_all_yearly_team_stats_already_in_db)
team_seasons_with_results = [x[0] for x in team_seasons_with_results_raw]

opponent_seasons_with_results_raw = db1.get_data(sql_queries.get_all_yearly_opponent_stats_already_in_db)
opponent_seasons_with_results = [x[0] for x in opponent_seasons_with_results_raw]

valid_seasons = helpers.valid_seasons

for season in valid_seasons:
    if season in team_seasons_with_results and season in opponent_seasons_with_results:
        print('season data has already been scraped: ' + str(season))
    else:
        try:
            season_data = yearly_team_stats_scrape.TeamStats(season[:3], season[3:]).get_results(api_connection = True)
            season_data['id'] = season
            team_per_game = season_data[season_data['player'] == 'Team/G']            
            opponent_per_game = season_data[season_data['player'] == 'Opponent/G']
            
            try:
                db1.insert_data("""INSERT INTO yearly_team_per_game_stats (player, mp, fg, fga, fg_pct, fg3, fg3a, fg3_pct, fg2,
                fg2a, fg2_pct, ft, fta, ft_pct, orb, drb, trb, ast,
                stl, blk, tov, pf, pts, team, year, id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, tuple(team_per_game.iloc[0].tolist()))
            
            except psycopg2.Error as error:
                print('Failed to insert data into yearly team stats table:', error)
            
            try:
                db1.insert_data("""INSERT INTO yearly_opponent_per_game_stats (player, mp, fg, fga, fg_pct, fg3, fg3a, fg3_pct, fg2,
                fg2a, fg2_pct, ft, fta, ft_pct, orb, drb, trb, ast,
                stl, blk, tov, pf, pts, team, year, id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, tuple(opponent_per_game.iloc[0]))

            except psycopg2.Error as error:
                print('Failed to insert data into yearly opponent stats table:', error)

        except psycopg2.Error as error:
                print('Other error:', error)

        print('Finished inserting game result data for ' + season)

db1.close()


