import os
from requests import Response
from komgapy.util import remove_duplicates
from PIL import Image
from smart_groups.util import *
from komgapy.wrapper.controllers import *
from komgapy import (
    KomgaSession,
    KomgaErrorResponse,
    KomgaSeries,
    KomgaBook,
    KomgaCollection,
    KomgaReadlist,
    )

from print_outputs import(
    print_item_data,
    print_has_poster_asset
)


def _post_user_generated_item(
        controller: Readlists | Collections,
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
    if isinstance(controller, Readlists):
        item_type = 'readlists'
    elif isinstance(controller, Collections):
        item_type = 'collections'

    item_data = make_user_generated_item_data(item_type, item_name, content_list, item_prefix, ordered)


    response = controller.new(item_data)


    item = update_if_item_already_exists(controller, response, item_prefix + item_name, item_data, overwrite)


    print_item_data(item)


    return item



def _add_item_poster(
        controller: Readlists | Collections,
        item: KomgaCollection| KomgaReadlist| KomgaBook| KomgaSeries,
        file_name: str,
        item_category: str,
        asset_dir: str,
        overlay_mode: str = 'no_asset'
        ) -> None:
    '''
    Add poster thumbnail to Komga item.
    Will add overlay to thumbnail depending on overlay_mode
    
    :param overlay_mode: 'no_asset', 'force', 'disable'
    '''

    if isinstance(controller, Readlists):
        item_type = 'readlists'
    elif isinstance(controller, Collections):
        item_type = 'collections'


    poster_dir = os.path.join(asset_dir, item_type)
        

    if item_category != None and os.path.exists(os.path.join(poster_dir, item_category)):
        poster_dir =os.path.join(poster_dir, item_category)


    poster_file_name = get_poster_file_name(file_name, poster_dir)


    current_image = controller.poster(item.id)
    

    if poster_file_name != None:      
        print_has_poster_asset(True)

        poster_file_path = os.path.join(poster_dir, poster_file_name)


        if overlay_mode == 'force':
            overlay_path = get_overlay_path(item_type, item_category, asset_dir)
            
            if overlay_path != None:
                print('Using Overlay')
                image = Image.open(poster_file_path)
                image = add_overlay(overlay_path, image)
                upload_image_object(controller, item_type, item.id, image)
                return None
            
            else:
                print('No overlay file found')


        if current_image == Image.open(poster_file_path):
            print('Poster Already Uploaded')

        else:
            controller.update_poster(item.id, poster_file_path)

    else:
        print_has_poster_asset(False)

        if overlay_mode in ['no_asset', 'force']: 
            overlay_path = get_overlay_path(item_type, item_category, asset_dir)
            
            if overlay_path != None:
                print('Using Overlay')
                image = add_overlay(overlay_path, current_image)
                if overlay_mode == 'force' or image._size != current_image._size:
                      upload_image_object(controller, item.id, image)  

                else:
                    print('Already has custom poster')

            else:
                print('No overlay file found')



def _update_existing_item(
        controller: Readlists | Collections,
        data: dict,
        item: KomgaReadlist|KomgaCollection| None = None,
        item_id: str| None = None,
        item_name: str| None = None,
        overwrite: bool = False
        ):
    '''
    Updates a collection or readlist from data

    :param data: dictionary of data to be updated(see docs for keys).
    :param overwrite: True replaces old data with new data, False appends new data to old data.
    '''
    
    if item == None:

        if item_id != None:
            item = controller.get(item_type, item_id)

        elif item_name != None:
            item = controller.get(item_type, item_name=item_name)

        else:
            raise Exception("No object, id, or name")


    if isinstance(controller, Readlists):
        item_type = 'readlists'
        data_key = 'bookIds'
        current_id_list = item.book_ids        
    elif isinstance(controller, Collections):
        item_type = 'collections'
        data_key = 'seriesIds'
        current_id_list = item.series_ids  


    item_id = item.id
    id_list: list = data[data_key]

    if overwrite != True:
        id_list += current_id_list
        data[data_key] = remove_duplicates(id_list)

    if sorted(data[data_key]) != sorted(current_id_list):
        r = controller.overwrite(item_type, item_id, data)
        # print(r)

        print('Item Updated')

        item = controller.get(item_type, item_id)
    else:

        print('Nothing to Update')

    return item


#---------


def update_if_item_already_exists(
        controller: Readlists | Collections,
        response: KomgaCollection|KomgaReadlist|KomgaErrorResponse,
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

                item = controller.get(name=item_name)

                item = _update_existing_item(controller, data, item, overwrite=overwrite)

            else:
                raise Exception(KomgaErrorResponse.message)
                return response
            
        else: 
            print("Item Doesn't Exist")
            item = response
        
        return item


def content_list_from_search_params(controller: Books | Series, search_params: dict):
    if isinstance(search_params, list):
        content_list = []
        for sp in search_params:
            if 'unpaged' not in sp:
                sp['unpaged'] = True 
            content_list.extend(controller.search(sp).content)

    else:
        if 'unpaged' not in search_params:
            search_params['unpaged'] = True 
        content_list = controller.search( search_params).content

    return content_list


def get_overlay_path(item_type: str, item_category: str, asset_dir: str):

    if item_category != None and os.path.exists(os.path.join(asset_dir, item_type, item_category, 'overlay.png')):
        return os.path.join(asset_dir, item_type, item_category, 'overlay.png')
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


def upload_image_object(controller: Readlists|Collections, item_id: str, image: Image.Image):
    if not os.path.exists('temp'):
        os.mkdir('temp')
    image.save('temp/temp.png')
    controller.update_poster(item_id, 'temp/temp.png')
    os.remove('temp/temp.png')
    os.removedirs('temp')


def determine_poster_file_path(item_type: str, item_category: str, asset_dir: str):

    poster_dir = os.path.join(asset_dir, item_type)
    
    if item_category != None and os.path.exists(os.path.join(poster_dir, item_category)):
        poster_dir = os.path.join(poster_dir, item_category)
    
    return poster_dir



