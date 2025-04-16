from db.all_db_stuff import *
from db.sql_queries import *
from scraping import helpers

import pandas as pd
import random

# all df code can go here
# 1. calls that put data into a dataframe
# 2. train test split
#

game_results_columns = ['id',
    'visitor',
    'home',
    'dates',
    'visitor_score',
    'home_score']

yearly_team_stats_columns = ['id',
    'player',
    'mp', 
    'fg', 
    'fga', 
    'fg_pct', 
    'fg3', 
    'fg3a', 
    'fg3_pct',
    'fg2', 
    'fg2a', 
    'fg2_pct', 
    'ft', 
    'fta', 
    'ft_pct', 
    'orb', 
    'drb', 
    'trb',
    'ast', 
    'stl', 
    'blk', 
    'tov', 
    'pf', 
    'pts', 
    'team', 
    'year']

yearly_opponent_stats_columns = ['id',
    'player',
    'mp', 
    'fg', 
    'fga', 
    'fg_pct', 
    'fg3', 
    'fg3a', 
    'fg3_pct',
    'fg2', 
    'fg2a', 
    'fg2_pct', 
    'ft', 
    'fta', 
    'ft_pct', 
    'orb', 
    'drb', 
    'trb',
    'ast', 
    'stl', 
    'blk', 
    'tov', 
    'pf', 
    'pts', 
    'team', 
    'year']

def sql_to_df(sql_query, df_columns):
    postgres_config_params = DatabaseConfig(filename = 'db/database.ini', section = 'postgresql').get_config_params()
    db_conn = Database(postgres_config_params)
    db_conn.connect()
    sql_data = db_conn.get_data(sql_query)
    sql_results_df = pd.DataFrame(sql_data, columns = df_columns)
    db_conn.close()
    sql_results_df.drop_duplicates(inplace = True)
    return sql_results_df

all_game_results_df = sql_to_df(get_all_game_results_data, game_results_columns)

team_per_game_stats_df = sql_to_df(get_all_yearly_team_stats_data, yearly_team_stats_columns)
team_per_game_stats_df = team_per_game_stats_df[['fg3a', 'fg3_pct', 'fg2a', 'fg2_pct', 'fta', 'ft_pct', 'orb', 'drb', 'ast', 'stl', 'blk', 'tov', 'pf', 'team', 'year']].copy()

opponent_per_game_stats_df = sql_to_df(get_all_yearly_opponent_stats_data, yearly_opponent_stats_columns)
opponent_per_game_stats_df = opponent_per_game_stats_df[['fg3a', 'fg3_pct', 'fg2a', 'fg2_pct', 'fta', 'ft_pct', 'orb', 'drb', 'ast', 'stl', 'blk', 'tov', 'pf', 'team', 'year']].copy()

def team_vs_opp_stats(team, season_year) :
    return np.subtract(np.array(team_per_game_stats_df[(team_per_game_stats_df['team'] == team) & (team_per_game_stats_df['year'] == season_year)].iloc[:,:-2]), np.array(opponent_per_game_stats_df[(opponent_per_game_stats_df['team'] == team) & (opponent_per_game_stats_df['year'] == season_year)].iloc[:,:-2]))

def diff_stats(team_a, team_b, season_year) : return np.subtract(np.array(team_per_game_stats_df[(team_per_game_stats_df['team'] == team_a) & (team_per_game_stats_df['year'] == season_year)].iloc[:,:-2]), np.array(team_per_game_stats_df[(team_per_game_stats_df['team'] == team_b) & (team_per_game_stats_df['year'] == season_year)].iloc[:,:-2]))

team_stats_diff_df = pd.DataFrame(data = team_per_game_stats_df.apply(lambda x: pd.Series(team_vs_opp_stats(x.team, x.year)[0], index = team_per_game_stats_df.iloc[:,:-2].columns), axis = 1), columns = team_per_game_stats_df.iloc[:,:-2].columns)

def game_results_cleaning():
    random_indexes = random.sample(range(len(all_game_results_df)), k = len(all_game_results_df)//2)
    all_game_results_df.loc[random_indexes,'team_a'] = all_game_results_df.loc[random_indexes,'visitor']
    all_game_results_df.loc[random_indexes,'team_b'] = all_game_results_df.loc[random_indexes,'home']
    all_game_results_df.loc[all_game_results_df['team_a'].isna(),'team_a'] = all_game_results_df.loc[all_game_results_df['team_a'].isna(),'home']
    all_game_results_df.loc[all_game_results_df['team_b'].isna(),'team_b'] = all_game_results_df.loc[all_game_results_df['team_b'].isna(),'visitor']

    all_game_results_df['team_a_is_home'] = (all_game_results_df['team_a'] == all_game_results_df['home']).astype(int)
    all_game_results_df['team_a_score'] = (all_game_results_df['team_a_is_home'] * all_game_results_df['home_score']) + (([1 - all_game_results_df['team_a_is_home']][0]) * all_game_results_df['visitor_score'])
    all_game_results_df['team_b_score'] = (all_game_results_df['team_a_is_home'] * all_game_results_df['visitor_score']) + (([1 - all_game_results_df['team_a_is_home']][0]) * all_game_results_df['home_score'])
    all_game_results_df['team_a_win'] = (all_game_results_df['team_a_score'] > all_game_results_df['team_b_score']).astype(int)
    all_game_results_df['season_year'] = (all_game_results_df.loc[:,'dates'] // 10000) + ((all_game_results_df.loc[:,'dates'] % 10000) // 100) // 8
    all_game_results_df['is_reg_season'] = all_game_results_df.apply(lambda x: (x.dates >= helpers.regular_season_dates[x.season_year][0]) & (x.dates <= helpers.regular_season_dates[x.season_year][1]), axis = 1)
    combined_game_df = all_game_results_df.loc[all_game_results_df['is_reg_season'] == True, ['team_a', 'team_b', 'season_year', 'dates', 'team_a_is_home', 'team_a_win']].copy()
    combined_game_df['team_stats_diff'] = combined_game_df.apply(lambda x: diff_stats(x.team_a, x.team_b, x.season_year), axis = 1)
    combined_game_df2 = combined_game_df[combined_game_df['team_stats_diff'].apply(len) > 0].copy()
    combined_game_df2[team_per_game_stats_df.iloc[:,:-2].columns.tolist()] = combined_game_df2.team_stats_diff.apply(lambda x: x[0]).tolist()
    cleaned_df = combined_game_df2[['fg3a', 'fg3_pct', 'fg2a', 'fg2_pct', 'fta', 'ft_pct', 'orb', 'drb', 'ast', 'stl', 'blk', 'tov', 'pf', 'team_a_is_home', 'team_a_win']]

    return cleaned_df

def train_test_split():
    pass

if __name__ == "__main__":
    #print(sql_to_df(get_all_yearly_team_stats_data, yearly_opponent_stats_columns).head())
    #print(game_results_cleaning().head())
    #print(team_vs_opp_stats('BOS', 2023))
    #for column in val2.columns:
    #    print(column + ": " + str(type(val2.loc[0, column])))

    #print(team_per_game_stats_df[(team_per_game_stats_df['team'] == 'TOR') & (team_per_game_stats_df['year'] == 2014)].iloc[:,:-5])
    print(game_results_cleaning().head)