import pandas as pd
import re
import math
from tqdm import tqdm
import spacy

nlp = spacy.load('en_core_web_sm')

platforms = set(pd.read_csv("data/platforms_list.txt", sep =  '\n', header=None, dtype = 'str', squeeze = True).apply(lambda x: x.lower()))

pronouns = ['i', "i'm", "i've", 'he', 'she', 'they', 'you', 'me', 'her', 'him', 'them']


def has_platform(post, platform_list = platforms):
    ''' Pre-filtering function to check that a post contains the name of one of the pre-established platforms
    
    Args:
        post (str): text of the post to check
        platform_list (list(str)): by default the list of platform in the data folder but can be changed to anything
    
    Returns:
        True if the post contains one of the platforms in the list, False otherwise. 
    '''
    return len(set(post.lower().split()) & platforms) > 0

def extract_platform(post, regex_platform, platform_list = platforms):
    ''' Extracts the platform name in the post (case insensitive), depending on the given regular expression

    Args:
        post (str): text of the post from which we extract the platform
        regex_platform (str): regular expression to capture the platform name (case insensitive)
        platform_list (list(str)): by default the list of platform in the data folder but can be changed to anything
    
    Returns:
        platform name if a match is found with the regex and it corresponds to one of the platforms in platform_list, 
        None otherwise
    '''
    plat = re.search(regex_platform, post, re.IGNORECASE)
    if plat:
        platform = plat.group(1).lower()
        if (platform in platform_list):
            return platform
    return None


def extract_entity(post, entity_regex, entity_first = True, pronouns_list = pronouns):
    ''' Extracts the entity in the post, depending on the given regular expression. The entity is composed of all the captured consecutive words that are nouns (and not pronouns) and which start with a capital letter. For eg: 'Donald Trump was banned from' will return Donald Trump whereas 'president Trump was banned from' will return Trump and 'Donald Trump the president was banned from' will return None.
    
    Args:
        post (str): text of the post to check
        entity_regex (str): regular expression to capture entity group
        entity_first (bool): if the entity comes first in the pattern
        pronouns_list (list(str)): list of pronouns to remove from entity group
        
    Returns:
        entity name if an entity is captured with the Regex, is a noun but not a pronoun and starts with a capital letter. 
        None otherwise.
    '''
    
    ent = re.search(entity_regex, post, re.IGNORECASE)
    if ent:
        doc = nlp(ent.group(1))
        tokens = [token.text for token in doc]
        entities = ''
        
        if entity_first:
            # Select all the consecutive words with uppercase letters starting at the rightmost word
            while(tokens[-1][0].isupper()):
                entities = tokens[-1] + ' ' + entities
                tokens = tokens[0:-1]
                if len(tokens) == 0:
                    break
        else:
            # Select all the consecutive words with uppercase letters starting at the leftmost word
            while(tokens[0][0].isupper()):
                entities = entities + ' ' + tokens[0]
                tokens = tokens[1:]
                if len(tokens) == 0:
                    break

        # Filter words to take only nouns and not pronouns
        doc2 = nlp(entities)
        res = ''
        for chunks in doc2.noun_chunks:
            if chunks.text.lower() not in pronouns_list:
                res = res + chunks.text
        if len(res) > 0:
            return res
        else:
            return None
    else:
        return None
    
