import pandas as pd
import json
import gzip
import io

def read_lines(month, year, filtr):
    ''' Read and selects lines that pass the filtr for reddit posts in the selected month and year.
    '''
    file = f'/dlabdata1/reddit_rad/{year}-{month}.jsonl.gz'
    data = []
    errors = 0
    good = 0
    print(f"Processing the file {file}")
    gz = gzip.open(file, 'rb')
    f = io.BufferedReader(gz)
    for i, line in enumerate(f):
        if(i%100000==0): print(i)
        if(errors%100000==0 and errors!=0): print('error')
        try:
            a = json.loads(line)
            title = a['title']
            if filtr(title):
                data.append([title, a['created_utc']])
                good = good + 1
        except Exception as e:
            print(e)
            errors = errors + 1
            pass
    print(f"there are {errors} errors and {good} matches")
    return data

def in_dict(s, entities_list, entities_dict):
    ''' Checks if a text s contains en entity (in entities_list) and its associated platforms (in entities_dict)
    '''
    matches = {x for x in entities_list if x in s}
    if len(matches) == 0:
        return False
    for m in matches:
        if entities_dict[m] in s.lower():
            return True
    return False

