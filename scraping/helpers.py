from datetime import date, timedelta

regular_season_dates = {
  2000: [19991031, 20000416],
  2001: [20001031, 20010418],
  2002: [20011030, 20020417],
  2003: [20021029, 20030416],
  2004: [20031028, 20040414],
  2005: [20041102, 20050420],
  2006: [20051101, 20060419],
  2007: [20061031, 20070415],
  2008: [20071030, 20080416],
  2009: [20081028, 20090415],
  2010: [20091027, 20100414],
  2011: [20101026, 20110413],
  2012: [20111225, 20120426],
  2013: [20121030, 20130417],
  2014: [20131029, 20140416],
  2015: [20141028, 20150415],
  2016: [20151027, 20160413],
  2017: [20161025, 20170412],
  2018: [20171017, 20180411],
  2019: [20181016, 20190410],
  2020: [20191022, 20200311],
  2021: [20201222, 20210716],
  2022: [20211019, 20220410],
  2023: [20221018, 20230409],
  2024: [20231024, 20230414],
  2025: [20241028, 20250413]
}

playoff_dates = {
  2000: [20000421, 20000619],
  2001: [20010420, 20010615],
  2002: [20020419, 20020616],
  2003: [20030418, 20030615],
  2004: [20040416, 20040615],
  2005: [20050423, 20050623],
  2006: [20060421, 20060620],
  2007: [20070420, 20070614],
  2008: [20080418, 20080617],
  2009: [20090418, 20090614],
  2010: [20100417, 20100617],
  2011: [20110416, 20110612],
  2012: [20120428, 20120621],
  2013: [20130420, 20130620],
  2014: [20140419, 20140615],
  2015: [20150418, 20150616],
  2016: [20160416, 20160619],
  2017: [20170415, 20170612],
  2018: [20180414, 20180608],
  2019: [20190413, 20190613],
  2020: [20200817, 20201011],
  2021: [20210522, 20210720],
  2022: [20220416, 20220616],
  2023: [20230415, 20230618],
  2024: [20240420, 20240616],
  2025: [20250418, 20250615]
}

valid_game_days = []

start_date = date.today() 
end_date = date(1999, 10, 31)    # perhaps date.today()

delta = start_date - end_date   # returns timedelta

for i in range(delta.days + 1):
    day = str(start_date - timedelta(days=i))
    day = int(day.replace("-", ""))
    month = (day // 100) % 100
    year = day // 10000
    if month > 8 and day >= regular_season_dates[year + 1][0]:
        valid_game_days.append(day)
    elif day <= playoff_dates[year][1]:
        valid_game_days.append(day)

nba_teams_by_season = {
    '1999-2000': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SEA', 'SAC', 'LAC', 'GSW', 'DEN', 'VAN', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA'],
    '2000-2001': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SEA', 'SAC', 'LAC', 'GSW', 'DEN', 'VAN', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA'],
    '2001-2002': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SEA', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA'],
    '2002-2003': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SEA', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA'],
    '2003-2004': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SEA', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA'],
    '2004-2005': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SEA', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA'],
    '2005-2006': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SEA', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA'],
    '2006-2007': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SEA', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA'],
    '2007-2008': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SEA', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA'],
    '2008-2009': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC'],  # OKC (formerly SEA)
    '2009-2010': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC'],
    '2010-2011': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC'],
    '2011-2012': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC'],
    '2012-2013': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC'],
    '2013-2014': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC', 'NOP'],  # New Orleans Pelicans (formerly Hornets)
    '2014-2015': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC', 'NOP'],
    '2015-2016': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC', 'NOP'],
    '2016-2017': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC', 'NOP'],
    '2017-2018': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC', 'NOP'],
    '2018-2019': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC', 'NOP'],
    '2019-2020': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC', 'NOP'],
    '2020-2021': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC', 'NOP'],
    '2021-2022': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC', 'NOP'],
    '2022-2023': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC', 'NOP'],
    '2023-2024': ['PHO', 'DAL', 'LAL', 'SAS', 'MIN', 'UTA', 'POR', 'SAC', 'LAC', 'GSW', 'DEN', 'MEM', 'CHI', 'IND', 'MIL', 'CLE', 'TOR', 'NYK', 'BOS', 'DET', 'MIA', 'WAS', 'ORL', 'ATL', 'CHA', 'OKC', 'NOP'],
}