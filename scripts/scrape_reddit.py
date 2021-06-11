import pandas as pd
import requests
import json
from datetime import datetime

def scrape_pattern(query, pattern, min_date, max_date, path, count):
    ''' Scrape reddit posts' which titles contain the query. Save their titles, id, date, number of comments and score
    Args:
        query (str): scrape posts with titles containing {query}
        pattern (str): the pattern we are considering
        min_date (int): oldest post dates to scrape (in timestamp epoch format)
        max_date (int): youngest post dates to scrape (in timestamp epoch format)
        path (str): path to write the files (saved as pickle objects of pandas dataframes) (each file is 10000000 posts)
        count (int): first index for filename
    Returns:
        count_file: the number of files written on disk
    '''
    date = max_date
    count_file = count
    data = []
    while(date > min_date):
        url = f'https://api.pushshift.io/reddit/search/submission/?title=\"{str(query)}\"&size=100&before={date}'
        d = requests.get(url).json()['data']
        min_d = int(datetime.now().timestamp())
        for i in d:
            date_d = i['created_utc']
            data.append([i['title'], date_d, pattern, i['id'],  i['score'], i['num_comments']])
            min_d = min(date_d, min_d)
        date = min_d
        if(len(data) > 10000000):
            df = pd.DataFrame(data, columns = ['text', 'date', 'pattern', 'id', 'score', 'nb_comments'])
            df.to_pickle(f"{path}{count_file}.pkl")
            data = []
            count_file = count_file + 1
    df = pd.DataFrame(data, columns = ['text', 'date', 'pattern', 'id', 'score', 'nb_comments'])
    df.to_pickle(f"{path}{count_file}.pkl")
    count_file = count_file + 1
    return count_file

def scrape_pairs(entity, platforms, min_date, max_date, path, count):
    ''' Scrape reddit posts' which titles contain the entity and at least one of the platforms. Save their titles, id, date, number of comments and score
    Args:
        entity (str): scrape posts with titles containing the entity
        platforms (list(str)): keep posts with titles containing the platform
        min_date (int): oldest post dates to scrape (in timestamp epoch format)
        max_date (int): youngest post dates to scrape (in timestamp epoch format)
        path (str): path to write the files (saved as pickle objects of pandas dataframes) (each file is 10000000 posts)
        count (int): first index for filename
    Returns:
        count_file: the number of files written on disk
    '''
    date = max_date
    count_file = count
    data = []
    while(date > min_date):
        url = f'https://api.pushshift.io/reddit/search/submission/?title=\"{str(entity)}\"&size=100&before={date}'
        d = requests.get(url).json()['data']
        min_d = int(datetime.now().timestamp())
        for i in d:
            title = i['title']
            date_d = i['created_utc']
            p = [x for x in platforms if x in title.lower()]
            if len(p) > 0:
                data.append([entity, p, title, date_d, i['id'],  i['score'], i['num_comments']])
            min_d = min(date_d, min_d)
            date = min_d
        if(len(data) > 10000000):
            df = pd.DataFrame(data, columns = ['entity', 'platforms', 'text', 'date', 'id', 'score', 'nb_comments'])
            df.to_pickle(f"{path}{count_file}.pkl")
            data = []
            count_file = count_file + 1
    df = pd.DataFrame(data, columns = ['entity', 'platforms', 'text', 'date', 'id', 'score', 'nb_comments'])
    count_file = count_file + 1
    df.to_pickle(f"{path}{count_file}.pkl")
    return count_file

