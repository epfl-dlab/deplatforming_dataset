import pandas as pd

def extract_patterns(post, entity, platforms):
    ''' Extracts the substring between the entity and platform in the post.
    
    Args:
        post (str): title of the post in consideration
        entity (str): entity in consideration in the post
        platforms (list(str)): platforms in consideration in the post
    
    Raises:
        ValueError if the entity or the platform don't appear in the post
        
    Returns:
        pattern: the substring between the entity and the pattern, with placeholder for the entity and pattern
    '''
    text = post.lower()
    ent = text.find(entity)
    results = []
    for platform in platforms:
        plat = text.find(platform)
        if ent < 0 or plat < 0:
            raise ValueError('The given entity and platforms are not in the post')
        if ent > plat:
            results.append(f"<plat>{text[plat + len(platform):ent]}<ent>")
        else:
            results.append(f"<ent>{text[ent + len(entity):plat]}<plat>")
    return results