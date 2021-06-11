from __future__ import print_function
import json
import urllib


def link_google_id(entity):
    ''' This method links the entity with its google id. To use this function, it is necessary to first generate an API key file
    with an associated google accounts (https://developers.google.com/knowledge-graph/prereqs).
    
    Args:
        entity (str): the entity for which we want to find the google id
    
    Returns:
        g_id (str): the g_id associated to the entity.
        None if there is no g_id associated with it.
    '''
    api_key = open('../deplatforming_dataset/.api_key').read()
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    data = []
    query = entity
    params = {
        'query': query,
        'limit': 10,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.parse.urlencode(params)
    response = json.loads(urllib.request.urlopen(url).read())
    max_score = 0
    # selects the element with the highest score
    for element in response['itemListElement']:
        score = element['resultScore']
        if score > max_score:
            max_score = score
            name = element['result']['name']
            itype = element['result']['@type']
            gid = element['result']['@id']
    if max_score>0:
        return gid
    return None