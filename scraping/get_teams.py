from bs4 import BeautifulSoup

import requests
import json
import pandas as pd
import numpy as np
import os
import re
import io
import lxml

class Teams:
    def __init__(self, team_page_to_check):
        self.team_page_to_check = team_page_to_check
        #'https://www.basketball-reference.com/teams/DAL/2024.html'    

    # this currently omits teams that no longer exist, ie the Supersonics
    def get_teams(self):
        teams_page_check = requests.get(self.team_page_to_check, params={'render_js': True})    
        teams_soup = BeautifulSoup(teams_page_check.text, 'lxml')

        teams_list = []

        for tag in teams_soup.find_all('div', {"class": "division"}):
            if tag.find('a') != None:
                for child_tag in tag.find_all('a'):
                    teams_list.append(child_tag.attrs['href'].split('/')[2])

        return teams_list
    
if __name__ == "__main__":
    team_check = Teams('https://www.basketball-reference.com/teams/DAL/2024.html')
    print(team_check.get_teams())