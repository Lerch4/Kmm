
def remove_duplicates(data: list) -> list:
    '''
    Takes a list and returms list with no duplicates
    '''
    data_no_dups = []
    for item in data:
        if item not in data_no_dups:
            data_no_dups.append(item)
    
    return data_no_dups


def check_key_exists(key: str, dictionary: dict, missing_return_value = None):
    
    if key in dictionary:    
        return dictionary[key]

    else:    
        return missing_return_value