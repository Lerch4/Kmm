

from smart_groups.generic_smart_group import(
     make_smart_user_generated_item,
     _add_item_poster,
     _update_existing_item,
     _post_user_generated_item,
     KomgaSession,
     check_key_exists
)
from requests import Response
from smart_groups.util import make_id_list, remove_blacklisted, make_prefix, remove_blacklisted_content


def update_existing_collection(session, data, collection = None, collection_id=None, collection_name = None, overwrite = False):

    return _update_existing_item(session, 'collections', data=data, item = collection, item_id = collection_id, item_name = collection_name, overwrite=overwrite)


def post_collection(session, collection_name, series_list, collection_prefix = '', ordered = False, overwrite = False):

    return _post_user_generated_item(session, 'collections', collection_name, series_list, collection_prefix, ordered, overwrite)


def add_collection_poster(session, collection, collection_name, collection_catagory):

    return _add_item_poster(session, 'collections', item= collection, item_name=collection_name, item_catagory=collection_catagory)


def make_smart_collection_old(
    session,
    search_params: dict = None,
    collection_prefix: str = None,
    collection_name: str = None,
    collection_catagory: str = None,
    series_ids: list = None,
    blacklisted_series_ids: list = None,
    blacklisted_search_params: dict = None,
    ordered = False,
    overwrite = False,
    collection_catagories = None,
    asset_dir = None
    ):
        make_smart_user_generated_item(
        session,
        'collections',
        collection_name,        
        search_params=search_params,
        item_prefix=collection_prefix,
        item_catagory=collection_catagory,
        content_id_list=series_ids,
        blacklisted_content_ids = blacklisted_series_ids,
        blacklisted_search_params=blacklisted_search_params,
        ordered=ordered,
        overwrite=overwrite,
        item_catagories=collection_catagories,
        asset_dir=asset_dir

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
    parent_collection_ids: list = [],
    parent_collection_names: list = [],
    ordered = False,
    overwrite = False,
    collection_catagories = None,
    asset_dir = None
):
         # trim name
        collection_name = collection_name.strip()
        
        # set default search params unless search_params explicitly set to None
        if search_params != None:
            if search_params == {}:
                search_params = {'search': f'"{collection_name}"'}
        
            if 'unpaged' not in search_params:
                search_params['unpaged'] = True 

            series_list = session._search('series', search_params).content

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
            blacklisted_series = session._search('series', blacklisted_search_params).content
            for series in blacklisted_series:
                blacklisted_series_ids.append(series.id)

        if blacklisted_series_ids != []:
            remove_blacklisted_content(series_ids, blacklisted_series_ids)


        collection_prefix = make_prefix(collection_prefix, collection_catagory, collection_catagories)


        # post collection and return collection data
        collection = _post_user_generated_item(session,'collections', collection_name, series_ids, collection_prefix, ordered, overwrite)


        if isinstance(collection, Response):
            print(collection.text)


        _add_item_poster(session,item_type='collections', item = collection, item_name = collection_name, item_catagory = collection_catagory, asset_dir=asset_dir)

