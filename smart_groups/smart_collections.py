from komgapy import KomgaSession, KomgaErrorResponse
from komgapy.exception_classes import NoSearchResults

from smart_groups.generic_smart_group import(
     make_smart_user_generated_item,
     _add_item_poster,
     _update_existing_item,
     _post_user_generated_item,
     check_key_exists,
     content_list_from_search_params
)
from requests import Response
from smart_groups.util import make_id_list, remove_blacklisted, make_prefix, remove_blacklisted_content


def update_existing_collection(
          session: KomgaSession,
          data: dict,
          collection: str = None,
          collection_id: str = None,
          collection_name: str = None,
          overwrite: bool = False
          ):
    '''
    Updates a collection from data

    :param data: dictionary of data to be updated(see docs for keys).
    :param overwrite: True replaces old data with new data, False appends new data to old data.
    '''

    return _update_existing_item(
         session,
         'collections',
         data = data,
         item = collection,
         item_id = collection_id,
         item_name = collection_name,
         overwrite = overwrite
         )


def post_collection(
          session: KomgaSession,
          collection_name: str,
          series_list: list[str],
          collection_prefix: str = '',
          ordered: bool = False,
          overwrite: bool = False
          ):
    '''
    '''

    return _post_user_generated_item(
         session,
         'collections',
         collection_name,
         series_list,
         collection_prefix,
         ordered,
         overwrite
         )


def add_collection_poster(
          session: KomgaSession,
          collection: str,
          collection_name: str,
          collection_catagory: str
          ):
    '''
    
    '''

    return _add_item_poster(
         session,
         'collections',
         item = collection,
         item_name = collection_name,
         item_catagory = collection_catagory
         )


def make_smart_collection(
    session: KomgaSession,
    search_params: dict = None,
    collection_prefix: str = None,
    collection_name: str = None,
    collection_catagory: str = None,
    series_ids: list = [],
    blacklisted_series_ids: list = [],
    blacklisted_search_params: dict = {},
    parent_collection_ids: list[str] = [],
    parent_collection_names: list[str] = [],
    ordered = False,
    overwrite = False,
    collection_catagories = None,
    asset_dir = None,
    overlay_mode: str = 'no_asset'
    ) -> None:
        '''
        Create a Komga collection based on input perameters.
        Then adds poster art or overlay from assets if available.
        If parameters are not used they are skipped.
        Best to mostly use 'search' param with Komga's Full Text Search (see docs)

        :param search_params: Dictionary of search parameters (see docs for keys).
        :param collection_prefix: Custom prefix for collection(overwrites catagory prefix).
        :param collection_catagory: Custom catagory that determines location of assets and prefix.
        :param series_ids: Komga series id list for series to be included in new data.
        :param blacklisted_series_ids: Komga series id list for series to be excluded from new data (Experimental).
        :param blacklisted_search_params: Search parameters for series to be excluded (Experminetal).
        :param parent_collection_ids: list of collection ids whose sereis will be added to new data(Experimental)
        :param parent_collection_names: List of collection names (exact with prefix) whose series will be added to new data(Experimental) 
        :param ordered: True keeps order while false sorts by alpha(Experminetal).
        :param overwrite: True replaces old content with new content while false appends new content to old content.
        '''
         # trim name
        collection_name = collection_name.strip()
        
        # set default search params unless search_params explicitly set to None
        if search_params != None:
            if search_params == {}:
                search_params = {'search': f'"{collection_name}"'}

            series_list = content_list_from_search_params(session, 'series', search_params)

            series_ids.extend(make_id_list(series_list))
        

        # add from parent collections
        if parent_collection_names != []:
             for collection_name in parent_collection_names:
                  parent_collection = session.get_collection(collection_name=collection_name)
                  parent_collection_ids.append(parent_collection.id)

        if parent_collection_ids != []:
             for collection_id in parent_collection_ids:
                  series_from_collection = session.series_in_collection(collection_id)

                  for series in series_from_collection:
                       series_ids.append(series.id)


        # remove blacklisted
        if blacklisted_search_params !={}:

            blacklisted_series = content_list_from_search_params(session, 'series', blacklisted_search_params)
            for series in blacklisted_series:
                blacklisted_series_ids.append(series.id)

        if blacklisted_series_ids != []:
           series_ids = remove_blacklisted_content(series_ids, blacklisted_series_ids)


        collection_prefix = make_prefix(collection_prefix, collection_catagory, collection_catagories)


        # post collection and return collection data
        if series_ids != []:
            collection = _post_user_generated_item(session,'collections', collection_name, series_ids, collection_prefix, ordered, overwrite)


            if isinstance(collection, Response):
                print(collection.text)
        else:
            try:
                collection = session.get_collection(collection_name=(collection_prefix + collection_name))

            except NoSearchResults:
                collection = None
                print('No existing collection and no search results found')
            
        if not isinstance(collection, KomgaErrorResponse) and collection != None:
            _add_item_poster(
                session,
                item_type = 'collections',
                item = collection,
                file_name = collection_name,
                item_catagory = collection_catagory,
                asset_dir = asset_dir,
                overlay_mode = overlay_mode
                )

