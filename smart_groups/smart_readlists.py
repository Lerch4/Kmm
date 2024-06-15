from smart_groups.generic_smart_group import(
    _add_item_poster,
    _update_existing_item,
    _post_user_generated_item,
    KomgaSession,
    check_key_exists
    
)
from requests import Response
from smart_groups.util import make_id_list, remove_blacklisted, make_prefix, remove_blacklisted_content

def update_existing_readlist(session, data, readlist = None, readlist_id=None, readlist_name = None, overwrite = False):

    return _update_existing_item(session, 'readlists', data=data, item = readlist, item_id = readlist_id, item_name = readlist_name, overwrite=overwrite)


def post_readlist(session, readlist_name, book_list, readlist_prefix = '', ordered = False, overwrite = False ):

    return _post_user_generated_item(session, 'readlists', readlist_name, book_list, readlist_prefix, ordered, overwrite)


def add_readlist_poster(session, readlist, readlist_name, readlist_catagory):

    return _add_item_poster(session, 'readlist', item=readlist, item_name=readlist_name, item_catagory=readlist_catagory)


# def make_smart_readlist_old(
#     session,
#     readlist_name: str,
#     search_params: dict = None,
#     book_search_params: dict = None,
#     readlist_prefix: str = None,
#     readlist_catagory: str = None,
#     book_ids: list = None,
#     blacklisted_book_ids: list = None,
#     blacklisted_search_params: dict = None,
#     ordered = False,
#     overwrite = False
#     ):

#     make_smart_user_generated_item_new(
#         session,
#         'readlists',
#         readlist_name,        
#         search_params,
#         book_search_params,
#         readlist_prefix,
#         readlist_catagory,
#         book_ids,
#         blacklisted_book_ids,
#         blacklisted_search_params,
#         ordered,
#         overwrite
#         )


def make_smart_readlist(
        session,
        readlist_name: str,
        readlist_catagory: str = None,
        series_search_params: dict = {},
        book_search_params: dict = {},
        readlist_prefix: str = None,
        book_ids: list = [],
        series_ids: list = [],
        blacklisted_book_ids: list = [],
        blacklisted_series_ids: list = [],
        blacklisted_book_search_params: dict = {},
        blacklisted_series_search_params: dict = {},
        ordered: bool = False,
        overwrite: bool = False,
        readlist_catagories = None,
        asset_dir = None
        ):
        '''
        Create or update readlist based on metadata of series or books

        :param search_params: dictionary of search parameters available for item type
        :param item_prefix: Prefix to be added to name for sorting
        :param item_name: Item name
        :param item_catagory: Catagory of item to be used for sorting, will be overridden by item_prefix
        :param content_id_list: List of content ids of content to be added
        :param blacklisted_content_ids: List of content ids of content to be excluded
        :param blacklisted_search_params: Search parameters for content to be excluded
        :param ordered: True keeps order while false sorts by alpha
        :param overwrite: True replaces old content with new content while false appends new content to old content
        '''
        # trim item name
        readlist_name = readlist_name.strip()

        if series_search_params == {} and book_search_params == {}:
            series_search_params = {'search': f'"{readlist_name}"'}

        elif series_search_params == None and book_search_params == {}:
            book_search_params = {'search': f'"{readlist_name}"'}
    

        book_list = []
        if len(book_search_params)>0:

            if 'unpaged' not in book_search_params:
                book_search_params['unpaged'] = True 

            book_list.extend(session._search('books', book_search_params).content)


        if len(series_search_params)>0:

            if 'unpaged' not in series_search_params:
                series_search_params['unpaged'] = True

            series_list = session._search('series', series_search_params).content
            series_ids.extend( make_id_list(series_list))
            for id in series_ids:
                    for book in session.books_in_series(id).content:
                        book_list.append(book)


        if book_list != []:
            book_ids.extend(make_id_list(book_list)) 


        # remove blacklisted
        if blacklisted_book_search_params != {} or blacklisted_series_search_params != {}:
            blacklisted_books = session._search('books', blacklisted_book_search_params).content
            blacklisted_series = session._search('series', blacklisted_series_search_params).content
            for series in blacklisted_series:
                blacklisted_series_ids.append(series.id)
            for series_id in blacklisted_series_ids:
                blacklisted_books.extend(session.books_in_series(series_id).content)
            for book in blacklisted_books:
                # if book.id not in blacklisted_book_ids:
                    blacklisted_book_ids.append(book.id)
    
        if blacklisted_book_ids != []:
            remove_blacklisted_content(book_ids, blacklisted_book_ids)

        readlist_prefix = make_prefix(readlist_prefix, readlist_catagory, readlist_catagories)

        # post collection and return collection data
        readlist = _post_user_generated_item(session,'readlists', readlist_name, book_ids, readlist_prefix, ordered, overwrite)

        if isinstance(readlist, Response):
            print(readlist.text)


        _add_item_poster(session,item_type='readlists', item = readlist, item_name = readlist_name, item_catagory = readlist_catagory, asset_dir=asset_dir) 
