#import psycopg2

from configparser import ConfigParser
#import pandas as pd

#import config

# DatabaseConfig(filename = 'database.ini', section = 'postgresql'):

class DatabaseConfig:
    def __init__(self, filename, section):
        self.filename = filename
        self.section = section

    def get_config_params(self):
        parser = ConfigParser()
        parser.read(self.filename)

        config_params = {}

        if parser.has_section(self.section):
            params = parser.items(self.section)

            for param in params:
                config_params[param[0]] = param[1]

        else:
            raise Exception('Section{0} is not found in the {1} file'.format(self.section, self.filename))
    
        return(config_params)
