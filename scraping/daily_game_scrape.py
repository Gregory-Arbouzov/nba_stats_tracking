from bs4 import BeautifulSoup
from dotenv import load_dotenv

import requests
import json
import pandas as pd
import numpy as np
import os
import re
import io
import lxml

load_dotenv()

SCRAPER_API_KEY=os.getenv('SCRAPER_API_KEY')

class GameResults:
    def __init__(self, date):
        self.date = date

    def get_results(self, api_connection):
        self.api_connection = api_connection

        year = self.date[:4]
        month = self.date[4:6]
        day = self.date[-2:]
    
        games_on_date_test_url = 'https://www.basketball-reference.com/boxscores/?month='  + str(int(month)) + '&day=' + str(int(day)) + '&year=' + str(int(year))

        if self.api_connection == None:
            games_on_date_test_page = requests.get(games_on_date_test_url,params={'render_js': True})
            #pass               

        else:
           payload = { 'api_key': SCRAPER_API_KEY, 'url': games_on_date_test_url, 'country_code': 'us', 'device_type': 'desktop', 'max_cost': '1000', 'session_number': '0', 'render_js': True}
           games_on_date_test_page = requests.get('https://api.scraperapi.com/', params=payload)


        game_on_date_test_soup = BeautifulSoup(games_on_date_test_page.text, 'lxml')

        winning_teams = []
        losing_teams = []
        winning_scores = []
        losing_scores = []
        home_teams = []

        for i in range(len(game_on_date_test_soup.find_all('tr', {"class": "winner"}))):
        
            winning_teams.append(game_on_date_test_soup.find_all('tr', {"class": "winner"})[i].find_all('td')[0].find('a').attrs['href'].split('/')[2])
            losing_teams.append(game_on_date_test_soup.find_all('tr', {"class": "loser"})[i].find_all('td')[0].find('a').attrs['href'].split('/')[2])

            winning_scores.append(int(game_on_date_test_soup.find_all('tr', {"class": "winner"})[i].find_all('td')[1].contents[0]))
            losing_scores.append(int(game_on_date_test_soup.find_all('tr', {"class": "loser"})[i].find_all('td')[1].contents[0]))

        for i in range(len(game_on_date_test_soup.find_all('tr', {'class':['winner', 'loser']}))):
            try:
                home_teams.append(game_on_date_test_soup.find_all('tr', {'class':['winner', 'loser']})[i].find('a', href=re.compile('/boxscores/')).attrs['href'].split('/')[2].split('.')[0][-3:])
            except:
                pass

        temp_df = pd.DataFrame({'home': home_teams, 'winning_team': winning_teams, 'losing_team': losing_teams, 'winning_score': winning_scores, 'losing_score': losing_scores})
        temp_df['visitor'] = temp_df.apply(lambda x: x.winning_team if x.winning_team != x.home else x.losing_team, axis = 1)
        temp_df['visitor_score'] = temp_df.apply(lambda x: x.winning_score if x.winning_team != x.home else x.losing_score, axis = 1)
        temp_df['home_score'] = temp_df.apply(lambda x: x.winning_score if x.winning_team == x.home else x.losing_score, axis = 1)
        temp_df['dates'] = self.date
        temp_df['id'] = temp_df['visitor'] + temp_df['home'] + temp_df['dates']

        final_df = temp_df[['id', 'visitor', 'home', 'dates', 'visitor_score', 'home_score']]
  
        return(final_df)
    
if __name__ == "__main__":
    test = GameResults('20230316')
    print(test.get_results(api_connection=True))