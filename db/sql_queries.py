


get_all_game_results_dates_already_in_db = """SELECT DISTINCT(dates) FROM game_results;"""

get_all_scrape_attempt_dates = """SELECT DISTINCT(dates) FROM game_dates_already_scraped;"""

get_all_yearly_team_stats_already_in_db = """SELECT DISTINCT(id) FROM yearly_team_per_game_stats;"""

get_all_yearly_opponent_stats_already_in_db = """SELECT DISTINCT(id) FROM yearly_opponent_per_game_stats;"""