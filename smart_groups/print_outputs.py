from komgapy import(
      KomgaCollection,
      KomgaReadlist,
      KomgaSeries,
      KomgaBook
)



# Print Functions --------------------------------------------------------------------------------------------------------------
def print_collection_input(collection_name, search_params, collection_prefix, collection_catagory, series_ids, blacklisted_series, blacklisted_search_params, ordered, overwrite):
        print(f'''
----------------------------------------------------------------------------------
                           New Collection - User Inputs
----------------------------------------------------------------------------------

collection_name: {collection_name}

search_params: {str(search_params)}

collection_prefix: {collection_prefix}

collection_catagory: {collection_catagory}

series_ids: {str(series_ids)}

blacklisted_series: {str(blacklisted_series)}

blacklisted_search_params: {str(blacklisted_search_params)}

ordered: {str(ordered)}

overwrite: {str(overwrite)}

----------------------------------------------------------------------------------
'''
    )

def print_has_poster_asset(has_poster_asset):

    if has_poster_asset == True:
        poster_asset_text = 'Has Poster Asset'
    else: 
        poster_asset_text = 'No Poster Asset'

    print(poster_asset_text)



def print_heading(heading_text):
    print(f'''
--------------------------------------
            {heading_text}
--------------------------------------
''')

def print_heading_from_item_type(item_type):
    match item_type:
        case 'collections': 
              print_heading('Collection')
        case 'readlists':
              print_heading('Readlist')


def print_item_data(item):
    if isinstance(item, KomgaCollection):
            item_type = 'Collection'
            content_type = 'Series'
            content_length = len(item.series_ids)
    elif isinstance(item, KomgaReadlist):
            item_type = 'Readlist'
            content_type = 'Books'
            content_length = len(item.book_ids)
    elif isinstance(item, KomgaSeries):
            item_type = 'Series'
            content_type = 'Books'
            content_length = item.media['pagesCount']
    elif isinstance(item, KomgaBook):
            item_type = 'Book'
            content_type = 'Pages'
            content_length = item.books_count
    else:
        return item
    
    print(f'''
{item_type} Name: {item.name}
{item_type} Id: {item.id}
{content_type}: {content_length}
''')




