# KomgaMetaManager (Kmm) 

Kmm is a script to help customize and organize your [Komga](https://komga.org/) server. It is loosly inspired by [Kometa (formerly Plex Meta Manager)](https://kometa.wiki/en/latest/). Kmm is still under development and has not been thoroughly tested. 

### Currently Kmm has the ability to
- Create / append collections(stable) and readlists(experimental)
    - 'Smart' collections and readlists (Based on search parameters from the Komga API).
    - Orginize created / managed collections and readlists into groups with prefixs automaticly being added to its name.
    - Add custom poster art for collections and readlists.
    - Add an overlay to custom or default poster art based on its collection or readlist group.



### Still too be Implemented
- [ ] Ability to add readlists from .cbl file
    - [ ] Ability to add community .cbl lists
- [ ] Add / edit / scrape series metadata (series.json)
- [ ] Add / edit / scrape book metadata (ComicInfo.xml)
- [ ] Add scheduling




## **Installation**
1. First download and install [KomgaPy](https://github.com/Lerch4/KomgaPy)
    - Currently KomgaPy has to be downloaded and installed manually
	    - Eventually will be added to PyPI
        - Download and extract repo and install repo to pip

2. Then Download and extract Kmm repo 
3. Finally install additional requirements
    - `pip install requirements.txt`

## **Usage**
- Set up config directory and config.yml file
    - Example config.yml
```
user: <your_username/email_here>
password: <your_password_here>
komga_url: <your_komga_server_url_here>

collection_catagories : 
  General      : '{0}: '
  Series Group : '{1}: '
  Characters   : '{2}: '
  Creators     : '{5}: '
  Publishers   : '{8}: '


smart_collections : 

# This will create a collection called {0}: Manga,
# with all series with reading direction set to right to left 
  - collection_name: Manga
    collection_catagory: General
    search_params:
      search: reading_direction:right_to_left

# This will create a collection called {1}: Hellboy,
# with all series returned from search for 'Hellboy' 
  - collection_name: Hellboy
    collection_catagory: Series Group

# This will create a collection called {2}: Nightwing,
# with all series returned from search for 'Nightwing' 
  - collection_name: Nightwing
    collection_catagory: Characters

# This will create a collection called {1}: Terminator,
# with all series returned from search for 'Terminator',
# except with series that include 'Deathstroke' or 'X-Terminators'
  - collection_name: Terminator
    collection_catagory: Series Group
    search_params: 
      search: '"Terminator" NOT ("Deathstroke" OR "X-Terminators")'

# This will create a collection called {8}: Image,
# with all series from publisher 'Image'
  - collection_name: Image
    collection_catagory: Publishers
    search_params:
      publisher: Image

# This will create a collection called {5}: Jack Kirby,
# with all series with Jack Kirby as penciller or writer
  - collection_name: Jack Kirby
    collection_catagory: Creators
    search_params:
      search: '((penciller:(Jack Kirby)) OR (writer:(Jack Kirby)))'

# This will create a collection called {5}: Jack Kirby,
# with all series with Alan Moore as writer
  - collection_name: Alan Moore
    collection_catagory: Creators
    search_params:
      author: Alan Moore, writer 
```
    
- Run Kmm.py

<!-- See [docs](./docs/) for further usage examples. -->
