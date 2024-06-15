
import os
from komgapy.util import remove_duplicates
from komgapy import (
    KomgaSession,
    KomgaErrorResponse,
    KomgaSearchResponse,
    KomgaSeries,
    KomgaBook,
    KomgaCollection,
    KomgaReadlist,
    )





# Supplimental Functions---------------------------------------------------------------------------------------------------------------------------

def get_poster_file_name(name: str, file_location: str) -> str | None:

    file_list = os.listdir(file_location)
    for file in file_list:
        if name == file[:-4]:
            return file
    return None


def make_id_list(item_list: list[KomgaSeries|KomgaCollection|KomgaBook|KomgaReadlist]) -> list[str]:
    id_list = []
    for item in item_list:
        id_list.append(item.id)

    return id_list


def replace_illegal_charactor(text: str) -> str:
    if ':' in text:
       text = text.replace(':', '-')

    return text


def remove_blacklisted(session: KomgaSession, content_type: str, id_list: list[str], blacklisted_content: list[str], blacklisted_search_params: dict) -> list[str]:
    if blacklisted_content != None:
        id_list = remove_blacklisted_content(id_list, blacklisted_content)

    if blacklisted_search_params != None:
        id_list = remove_blacklisted_search_params(session,content_type, id_list, blacklisted_search_params)
    
    return id_list


def remove_blacklisted_content(id_list: list[str], blacklisted_id_list: list[str]) -> list[str]:
    for id in id_list:
        if id in blacklisted_id_list:
            id_list.remove(id)

    return id_list


def remove_blacklisted_search_params(session: KomgaSession, content_type: str, id_list: list[str], blacklisted_search_params: dict) -> list[str]:

    blacklisted_series = session._search(content_type, blacklisted_search_params).content
    
    blacklisted_ids = make_id_list(blacklisted_series)

    return remove_blacklisted_content(id_list, blacklisted_ids)


def check_key_exists(key: str, dictionary: dict, missing_return_value = None):
    
    if key in dictionary.keys():    
        return dictionary[key]

    else:    
        return missing_return_value


def get_backup_name(search_params: dict) -> str | None:   
    if search_params != None:
        search = check_key_exists('search', search_params)
        if search != None:
            name = search['search']  
    else: return None        
    return name


def make_prefix(prefix: str, catagory: str, catagories: dict) -> str:
    if prefix == '' and catagory in catagories.keys():
        prefix = catagories[catagory]
    return prefix


# def remove_duplicates(data: list) -> list:
#     return list(set(data))


def make_content_id_key(item_type: str):

    match item_type :
        case 'collections':
            content_id_key = 'seriesIds'
        case 'readlists': 
            content_id_key = 'bookIds'

    return content_id_key


# def get_content_list(session, item_type, series_search_params, book_search_params):

#     if 'unpaged' not in series_search_params.keys():
#         series_search_params['unpaged'] = True 

#     match item_type:
#         case 'collections':
#             item_catagories = collection_catagories
#             content_list = session._search('series', series_search_params).content
            
#         case 'readlists':
#             item_catagories = readlist_catagories
#             content_list = []

#             if book_search_params != {}:
#                 if 'unpaged' not in book_search_params.keys():
#                     book_search_params['unpaged'] = True 
#                 content_list.extend(session._search('books', book_search_params).content)


#             if len(series_search_params)>1:
#                 series_list = session._search('series', series_search_params).content
#                 series_id_list = make_id_list(series_list)

#                 for id in series_id_list:
#                     for book in session.books_in_series(id).content:
#                         content_list.append(book)
    
    
#     return content_list



def make_user_generated_item_data(item_type, item_name, content_list, item_prefix, ordered= False, summary='') -> dict:
    data = {
        'name': item_prefix + item_name,
        'ordered': ordered,
        make_content_id_key(item_type): remove_duplicates(content_list),
        'summary': summary
    }

    return data




def get_item_type_str_title(item):
    
    if isinstance(item, KomgaCollection):
            return 'Collecction'
    elif isinstance(item, KomgaReadlist):
            return 'Readlist'
    elif isinstance(item, KomgaSeries):
            return 'Series'
    elif isinstance(item, KomgaBook):
            return 'Book'
    else:
        return item

