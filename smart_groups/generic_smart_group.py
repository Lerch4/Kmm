import os, io
from requests import Response
from komgapy.util import remove_duplicates
from PIL import Image, ImageDraw, ImageFont
from smart_groups.util import *

from komgapy import (
    KomgaSession,
    KomgaErrorResponse,
    KomgaSearchResponse,
    KomgaSeries,
    KomgaBook,
    KomgaCollection,
    KomgaReadlist,
    )

from smart_groups.print_outputs import(
    print_item_data,
    print_heading_from_item_type,
    print_has_poster_asset
)


def make_smart_user_generated_item(
        session,
        item_type: str,
        item_name: str,
        search_params: dict = None,
        item_prefix: str = None,
        item_catagory: str = None,
        content_id_list: list = None,
        blacklisted_content_ids: list = None,
        blacklisted_search_params: dict = None,
        ordered: bool = False,
        overwrite: bool = False,
        item_catagories = None,
        asset_dir = None
        ):
        '''
        Create or update collection or readlist based on metadata of series or books

        :param item_type: "collections" or "readlists"
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
        item_name = item_name.strip()


        if search_params == None:
            search_params = {'search': f'"{item_name}"'}
        
        if 'unpaged' not in search_params.keys():
            search_params['unpaged'] = True 


        match item_type:
            case 'collections':
                # item_catagories = collection_catagories
                content_type = 'series'

            case 'readlists':
                # item_catagories = readlist_catagories
                content_type = 'books'

            case _:
                raise Exception('Incopatable item type')
    
        

        item_prefix = make_prefix(item_prefix, item_catagory, item_catagories)


        content_list = session._search(content_type, search_params).content


        content_id_list = make_id_list(content_list)
    

        remove_blacklisted(session, content_type, content_id_list, blacklisted_content_ids, blacklisted_search_params)


        # post collection and return collection data
        item = _post_user_generated_item(session,item_type, item_name, content_id_list, item_prefix, ordered, overwrite)
        if isinstance(item, Response):
            print(item.text)

        _add_item_poster(session,item_type=item_type, item = item, item_name = item_name, item_catagory = item_catagory, asset_dir=asset_dir)


def _post_user_generated_item(
        session: KomgaSession,
        item_type: str,
        item_name: str,
        content_list: list[str],
        item_prefix: str = '',
        ordered: bool = False,
        overwrite: bool = False
        ):
    '''
    Post new item or update an exsisting item with new data.
    
    :param item_type: Includes user generated items such as collections or readlist
    :param item_name: Name of item 
    :param content_list: List of series ids(collection) or book ids(readlist) in item
    :param item_prefix: Prefix added to name to be used for sorting
    :param ordered: True will keep the order of the content list, while false will sort by alpha
    :param overwrite: True will replace existing content

    '''

    # print_heading_from_item_type(item_type)
    

    item_data = make_user_generated_item_data(item_type, item_name, content_list, item_prefix, ordered)


    response = session._add_new_user_generated_item(item_type, item_data)


    item = update_if_item_already_exists(session, response, item_type, item_prefix + item_name, item_data, overwrite)


    print_item_data(item)


    return item



def _add_item_poster(
        session,
        item_type: str,
        item,
        file_name: str,
        item_catagory: str,
        asset_dir: str,
        overlay_mode: str = 'no_asset'
        ) -> None:
    '''
    Add poster thumbnail to Komga item
    

    '''
    poster_dir = os.path.join(asset_dir, item_type)
        
    if item_catagory != None and os.path.exists(f'{poster_dir}\\{item_catagory}'):
        poster_dir += '\\' + item_catagory

    poster_file_name = get_poster_file_name(file_name, poster_dir)

    current_image = session._get_item_poster(item_type, item.id)
    
    if poster_file_name != None:      
        print_has_poster_asset(True)

        poster_file_path = os.path.join(poster_dir, poster_file_name)


        if overlay_mode == 'force':

            overlay_path = get_overlay_path(item_type, item_catagory, asset_dir)
            

            if overlay_path != None:
                print('Using Overlay')
                image = Image.open(poster_file_path)
                image = add_overlay(overlay_path, image)
                upload_image_object(session, item_type, item.id, image)
                return None
            else:
                print('No overlay file found')

        if current_image == Image.open(poster_file_path):
            print('Poster Already Uploaded')

        else:
            session._update_item_poster(item_type,item.id, poster_file_path)

    else:
        print_has_poster_asset(False)

        if overlay_mode in ['no_asset', 'force']: 
            overlay_path = get_overlay_path(item_type, item_catagory, asset_dir)
            

            if overlay_path != None:
                print('Using Overlay')
                image = add_overlay(overlay_path, current_image)
                if overlay_mode == 'force' or image._size != current_image._size:
                      upload_image_object(session, item_type, item.id, image)                  
                else:
                    print('Already has custom poster')

            else:
                print('No overlay file found')

def _update_existing_item(
        session: KomgaSession,
        item_type: str,
        data: dict,
        item: KomgaReadlist|KomgaCollection = None,
        item_id: str = None,
        item_name: str = None,
        overwrite: bool = False
        ):
    '''
    Updates a collection or readlist from data

    :param data: dictionary of data to be updated(see docs for keys).
    :param overwrite: True replaces old data with new data, False appends new data to old data.
    '''
    
    if item == None:

        if item_id != None:
            item = session._get_item(item_type, item_id)

        elif item_name != None:
            item = session._get_item(item_type, item_name=item_name)

        else:
            raise Exception("No object, id, or name")


    match item_type:
        case 'readlists':
            data_key = 'bookIds'
            current_id_list = item.book_ids
            
        case 'collections':
            data_key = 'seriesIds'
            current_id_list = item.series_ids
            
        case _:
            raise Exception('Incompatable item type')

    item_id = item.id
    id_list: list = data[data_key]

    if overwrite != True:
        id_list += current_id_list
        data[data_key] = remove_duplicates(id_list)

    if sorted(data[data_key]) != sorted(current_id_list):
        session._overwrite_existing_item(item_type, item_id, data)

        print('Item Updated')

        item = session._get_item(item_type, item_id)
    else:

        print('Nothing to Update')

    return item

#---------

def update_if_item_already_exists(
        session: KomgaSession,
        response: KomgaCollection|KomgaReadlist|KomgaErrorResponse,
        item_type: str,
        item_name: str,
        data: dict,
        overwrite: bool = False
        ) -> KomgaCollection | KomgaReadlist | KomgaErrorResponse:
        '''
        Takes the response from uploading a new collection or readlist.
        If the item already exists then the data is then updated to that item.

        :param response: The response from attempting to upload a new item
        '''
        
        if isinstance(response, KomgaErrorResponse):
            if 'name already exists' in response.message:
                print('Item Exists')

                item = session._get_item(item_type,item_name=item_name)

                item = _update_existing_item(session, item_type, data, item, overwrite=overwrite)

            else:
                raise Exception(KomgaErrorResponse.message)
                return response
            
        else: 
            print("Item Doesn't Exist")
            item = response
        
        return item



def content_list_from_search_params(session, item_type, search_params):
    if isinstance(search_params, list):
        content_list = []
        for sp in search_params:
            if 'unpaged' not in sp:
                sp['unpaged'] = True 
            content_list.extend(session._search(item_type, sp).content)

    else:
        if 'unpaged' not in search_params:
            search_params['unpaged'] = True 
        content_list = session._search(item_type, search_params).content

    return content_list




def get_overlay_path(item_type: str, item_catagory: str, asset_dir: str):

    if os.path.exists(os.path.join(asset_dir, item_type, item_catagory, 'overlay.png')):
        return os.path.join(asset_dir, item_type, item_catagory, 'overlay.png')
    elif os.path.exists(os.path.join(asset_dir, item_type, 'overlay.png')):
        return os.path.join(asset_dir, item_type, 'overlay.png')
    elif os.path.exists(os.path.join(asset_dir, 'overlay.png')):
        return os.path.join(asset_dir, item_type, 'overlay.png')
    else:
        return None
    

def add_overlay(overlay_path: str, current_image: Image.Image):
    # print('Using Default Overlay')
    overlay = Image.open(overlay_path)
    image = current_image
    size = image._size
    overlay.thumbnail(size)
    image = image.resize(overlay._size)
    # overlay = overlay.resize(size) 
    image.paste(overlay, (0,0), mask = overlay)
    
    return image


def upload_image_object(session, item_type: str, item_id: str, image: Image.Image):
    if not os.path.exists('temp'):
        os.mkdir('temp')
        image.save('temp/temp.png')
        session._update_item_poster(item_type, item_id, 'temp/temp.png')
        os.remove('temp/temp.png')
        os.removedirs('temp')


def determine_poster_file_path(item_type: str, item_catagory: str, asset_dir: str):

    poster_dir = os.path.join(asset_dir, item_type)
    
    if item_catagory != None and os.path.exists(f'{poster_dir}\\{item_catagory}'):
        poster_dir += '\\' + item_catagory

    return poster_dir



