from komgapy import(
      KomgaCollection,
      KomgaReadlist,
      KomgaSeries,
      KomgaBook
)

def print_has_poster_asset(has_poster_asset: bool) -> None:
    '''
    Print if poster asset is present
    '''

    if has_poster_asset == True:
        poster_asset_text = 'Has Poster Asset'
    else: 
        poster_asset_text = 'No Poster Asset'

    print(poster_asset_text)



def print_heading(text: str) -> None:
    '''
    Prints text as heading
    '''
    print(f'''
----------------------------------------
{text.center(40)}
----------------------------------------
''')

def print_heading_from_item_type(item_type: str) -> None:
    '''
    Print item type as heading
    '''
    match item_type:
        case 'collections': 
              print_heading('Collection')
        case 'readlists':
              print_heading('Readlist')


def print_item_data(item):
    '''
    Prints name, id, and content length for an item
    '''
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




def print_input_params(input_params):
    # print(f'Input Parameters: {json.dumps(input_params, indent=1)}\n')
    print('Input Parameters:')
    for k,v in input_params.items():
         print(f'{k}: {v}')
    print()

def print_start_new_group(item_type, input_params):
     print_heading_from_item_type(item_type)
     print_input_params(input_params)
     