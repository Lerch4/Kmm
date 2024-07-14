import os

from komgapy import KomgaReadlist, KomgaSession, KomgaErrorResponse
from smart_groups.generic_smart_group import(
    _add_item_poster,
    _update_existing_item,
    _post_user_generated_item,
    content_list_from_search_params
    
)
from requests import Response
from smart_groups.util import make_id_list, make_prefix, remove_blacklisted_content

def update_existing_readlist(
    session: KomgaSession,
    data: dict,
    readlist: KomgaReadlist = None,
    readlist_id: str = None,
    readlist_name: str = None,
    overwrite: bool = False
    ) -> KomgaReadlist:  

    return _update_existing_item(
        session,
        'readlists',
        data = data,
        item = readlist,
        item_id = readlist_id,
        item_name = readlist_name,
        overwrite=overwrite
        )


def post_readlist(
    session: KomgaSession,
    readlist_name: str,
    book_list: list[str],
    readlist_prefix: str = '',
    ordered: bool = False,
    overwrite: bool = False
    ) -> KomgaReadlist | KomgaErrorResponse: 

    return _post_user_generated_item(
        session,
        'readlists',
        readlist_name,
        book_list,
        readlist_prefix,
        ordered,
        overwrite
        )


def add_readlist_poster(
    session: KomgaSession,
    readlist: KomgaReadlist,
    readlist_name: str,
    readlist_category: str
    ) -> None:

    _add_item_poster(
        session,
        'readlist',
        item=readlist,
        item_name = readlist_name,
        item_category = readlist_category
        )


def make_smart_readlist(
    session: KomgaSession,
    readlist_name: str,
    readlist_category: str| None = None,
    series_search_params: dict| None = {},
    book_search_params: dict| None = {},
    readlist_prefix: str = '',
    book_ids: list = [],
    series_ids: list = [],
    blacklisted_book_ids: list = [],
    blacklisted_series_ids: list = [],
    blacklisted_book_search_params: dict = {},
    blacklisted_series_search_params: dict = {},
    ordered: bool = False,
    overwrite: bool = False,
    readlist_categories = None,
    asset_dir = None,
    cbl: str| list[str]| None = None,
    display_unmatched: bool = False,
    overlay_mode: str = 'no_asset',
    parent_readlist_ids: list[str] = [],
    parent_readlist_names: list[str] = [],
    ):
    '''
    Create or update readlist based on metadata of series or books

    :param search_params: dictionary of search parameters available for item type
    :param item_prefix: Prefix to be added to name for sorting
    :param item_name: Item name
    :param item_category: Catagory of item to be used for sorting, will be overridden by item_prefix
    :param content_id_list: List of content ids of content to be added
    :param blacklisted_content_ids: List of content ids of content to be excluded
    :param blacklisted_search_params: Search parameters for content to be excluded
    :param ordered: True keeps order while false sorts by alpha
    :param overwrite: True replaces old content with new content while false appends new content to old content
    '''
    # trim item name
    readlist_name = readlist_name.strip()
    # If has cbl use only that to make readlist, else check search params
    if cbl != None:
        if type(cbl) == str:
            cbl = [cbl]
           

        book_ids = []
        unmatched = []


        for l in cbl:

            if 'https://' in l:
                match_response = session.match_readlist_cbl_from_url(l)

            else:
                if l[:-4] != '.cbl': 
                    l += '.cbl'
                print(l)
                cbl_loc = os.path.join(asset_dir, 'cbl', str(l))
                match_response = session.match_readlist_cbl_from_path(cbl_loc)

            book_ids.extend(match_response.book_ids) 

            unmatched.extend(match_response.unmatched)

            ordered = True
            overwrite = True

            # print unmatched
            print('Matching cbl File')
            print(f'Number of Unmatched: {len(unmatched)}')
            if display_unmatched:
                for i in unmatched:
                    print(f"series: {i['series']}")
                    print(f"number: {i['number']}")
                    print()
            print()

    else:
        
        # set default search_params
        if series_search_params == {} and book_search_params == {}:
            series_search_params = {'search': f'"{readlist_name}"'}

        elif series_search_params == None and book_search_params == {}:
            book_search_params = {'search': f'"{readlist_name}"'}


        if 'unpaged' not in series_search_params:
            series_search_params['unpaged'] = True 

        if 'unpaged' not in book_search_params:
            book_search_params['unpaged'] = True 

        
        # if there are book search params search for them
        if book_search_params != {}:
            book_list = content_list_from_search_params(session, 'books', book_search_params)
        else: book_list = []

        # if there are series search params search for them 
        if series_search_params != {}:

            series_list = content_list_from_search_params(session, 'series', series_search_params)
            series_ids.extend( make_id_list(series_list))
            for id in series_ids:
                    for book in session.books_in_series(id).content:
                        book_list.append(book)

        # add searched book ids to book id list
        if book_list != []:
            book_ids.extend(make_id_list(book_list)) 



        # add from parent readlists
        if parent_readlist_names != []:
             for readlist_name in parent_readlist_names:
                  parent_readlist = session.get_readlist(readlist_name=readlist_name)
                  parent_readlist_ids.append(parent_readlist.id)

        if parent_readlist_ids != []:
             for readlist_id in parent_readlist_ids:
                  books_from_readlist = session.books_in_readlist(readlist_id)

                  for book in books_from_readlist:
                       book_ids.append(book.id)





        # remove blacklisted
        blacklisted_books = []
        if blacklisted_book_search_params != {}:
            blacklisted_books = content_list_from_search_params(session, 'books', blacklisted_book_search_params)

        if blacklisted_series_search_params != {}:
            blacklisted_series = content_list_from_search_params(session, 'series', blacklisted_series_search_params)

            for series in blacklisted_series:
                blacklisted_series_ids.append(series.id)


        if blacklisted_series_ids != []:
            for series_id in blacklisted_series_ids:
                blacklisted_books.extend(session.books_in_series(series_id).content)

        if blacklisted_books != []:
            for book in blacklisted_books:
                # if book.id not in blacklisted_book_ids:
                    blacklisted_book_ids.append(book.id)

        if blacklisted_book_ids != []:
           book_ids = remove_blacklisted_content(book_ids, blacklisted_book_ids)

    # determine prefix
    readlist_prefix = make_prefix(readlist_prefix, readlist_category, readlist_categories)


    # post readlist and return readlist data
    readlist = _post_user_generated_item(session,'readlists', readlist_name, book_ids, readlist_prefix, ordered, overwrite)





    # if response was to able to be converted print response
    if isinstance(readlist, Response):
        print(readlist.text)


    _add_item_poster(
        session,
        item_type='readlists',
        item = readlist,
        file_name = readlist_name,
        item_category = readlist_category,
        asset_dir=asset_dir,
        overlay_mode = overlay_mode
        ) 
