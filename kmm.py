import os

from config_adapter import config
from komgapy import KomgaSession
from smart_groups.smart_collections import make_smart_collection, check_key_exists
from smart_groups.smart_readlists import make_smart_readlist
from smart_groups.print_outputs import print_start_new_group


asset_dir = check_key_exists('asset_dir', config, os.path.join(os.path.dirname(__file__), 'config', 'assets'))
smart_collections = check_key_exists('smart_collections', config, [])
collection_catagories = check_key_exists('collection_catagories', config, [])
smart_readlists = check_key_exists('smart_readlists', config, [])
readlist_catagories = check_key_exists('readlist_catagories', config, [])


def run_smart_collections(session: KomgaSession, asset_dir=asset_dir) -> None:
    '''
    Make collection for every entry in smart_collections in config file
    '''
    for collection in smart_collections:

        print_start_new_group('collections', collection)

        make_smart_collection(
            session,
            collection_name=check_key_exists('collection_name', collection),
            search_params=check_key_exists('search_params', collection, {}),
            collection_prefix=check_key_exists('collection_prefix', collection),
            collection_catagory=check_key_exists('collection_catagory', collection),
            series_ids=check_key_exists('series_ids', collection, []),
            blacklisted_series_ids=check_key_exists('blacklisted_series_ids', collection, []),
            blacklisted_search_params=check_key_exists('blacklisted_search_params', collection, {}),
            parent_collection_ids=check_key_exists('parent_collection_ids', collection, []),
            parent_collection_names=check_key_exists('parent_collection_names', collection, []),
            ordered=check_key_exists('ordered', collection, False),
            overwrite=check_key_exists('overwrite', collection, False),
            collection_catagories=collection_catagories,
            asset_dir=asset_dir,
            overlay_mode=check_key_exists('overlay_mode', collection,'no_asset')
            )
        


def run_smart_readlists(session: KomgaSession, asset_dir=asset_dir) -> None:
    '''
    Make readlist for every entry in smart_readlists in config file
    '''
    for readlist in smart_readlists:

        print_start_new_group('readlists', readlist)

        make_smart_readlist(
                session,
                readlist_name=check_key_exists('readlist_name', readlist),
                readlist_catagory=check_key_exists('readlist_catagory', readlist),
                series_search_params=check_key_exists('search_params', readlist, {}),
                book_search_params=check_key_exists('book_search_params', readlist, {}),
                readlist_prefix=check_key_exists('readlist_prefix', readlist, ''),
                book_ids=check_key_exists('blacklisted_book_ids', readlist, []),
                series_ids=check_key_exists('series_ids', readlist, []),
                blacklisted_book_ids=check_key_exists('blacklisted_book_ids', readlist, []),
                blacklisted_book_search_params=check_key_exists('blacklisted_book_search_params', readlist, {}),
                blacklisted_series_search_params=check_key_exists('blacklisted_series_search_params', readlist, {}),
                ordered= check_key_exists('ordered', readlist, False),
                overwrite = check_key_exists('overwrite', readlist, False),
                readlist_catagories= readlist_catagories,
                asset_dir = asset_dir
                )


# _____________________________________________________________________________________________________

if __name__ == '__main__':
    session = KomgaSession(config['komga_url'], (config['user'], config['password']))
    run_smart_collections(session)
    run_smart_readlists(session)
    