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

class TeamStats:
    def __init__(self, team, year):
        self.team = team
        self.year = year

    def get_results(self, api_connection):
        self.api_connection = api_connection

        team_stats_summary_url = 'https://www.basketball-reference.com/teams/' + self.team + '/' + self.year + '.html'
        team_stats_summary_page = requests.get(team_stats_summary_url, params={'render_js': True})    

        team_stats_df_names = []
            
        if self.api_connection == None:
            team_stats_summary_page = requests.get(team_stats_summary_url,params={'render_js': True})
            
        else:
            payload = { 'api_key': SCRAPER_API_KEY, 'url': team_stats_summary_url, 'country_code': 'us', 'device_type': 'desktop', 'max_cost': '1000', 'session_number': '0', 'render_js': True}
            team_stats_summary_page = requests.get('https://api.scraperapi.com/', params=payload)

        team_soup = BeautifulSoup(team_stats_summary_page.text, 'lxml')

        team_vs_opp_stats = []
        team_vs_opp_column_names = []

        try:
            for i in range(len(team_soup.find('div',id = 'all_team_and_opponent').contents[4].split(' '))):
                if 'data-stat' in team_soup.find('div',id = 'all_team_and_opponent').contents[4].split(' ')[i]:
                    if "scope" in team_soup.find('div',id = 'all_team_and_opponent').contents[4].split(' ')[i+1].split('<')[0].strip('>'):
                        pass
                    elif team_soup.find('div',id = 'all_team_and_opponent').contents[4].split(' ')[i+1].split('<')[0].strip('>') == '':
                        pass
                    elif team_soup.find('div',id = 'all_team_and_opponent').contents[4].split(' ')[i+1].split('<')[0].strip('>') == 'Year/Year':
                        pass
                    elif team_soup.find('div',id = 'all_team_and_opponent').contents[4].split(' ')[i].strip('data-stat=') == '"g"':
                        #games_played = team_soup.find('div',id = 'all_team_and_opponent').contents[4].split(' ')[i+1].split('<')[0].strip('>')
                        pass
                    else:
                        team_vs_opp_stats.append(team_soup.find('div',id = 'all_team_and_opponent').contents[4].split(' ')[i+1].split('<')[0].strip('>'))
                        team_vs_opp_column_names.append(team_soup.find('div',id = 'all_team_and_opponent').contents[4].split(' ')[i].strip('data-stat='))
                        #print(team_soup.find('div',id = 'all_team_and_opponent').contents[4].split(' ')[i].strip('data-stat='), " : ", team_soup.find('div',id = 'all_team_and_opponent').contents[4].split(' ')[i+1].split('<')[0].strip('>'))
        
            team_vs_opp_column_names_unique = [name.strip('"') for name in team_vs_opp_column_names[:23]]
            
            team_vs_opp_df = pd.DataFrame(team_vs_opp_stats)

            reshaped_team_vs_opp_df = pd.DataFrame(np.reshape(team_vs_opp_df.values,(-1,23)))
            reshaped_team_vs_opp_df.columns = team_vs_opp_column_names_unique
            reshaped_team_vs_opp_df['team'] = self.team
            reshaped_team_vs_opp_df['year'] = self.year

            all_team_stats_df = pd.concat([all_team_stats_df,reshaped_team_vs_opp_df])
            
        except:
            print('Error: ' + self.team + '_' + str(self.year))