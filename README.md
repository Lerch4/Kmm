# KomgaMetaManager (Kmm) 

Kmm is a script to help customize and organize your [Komga](https://komga.org/) server. It is loosly inspired by [Kometa (formerly Plex Meta Manager)](https://kometa.wiki/en/latest/). Kmm is still under development and has not been thoroughly tested. 

### Currently Kmm has the ability to
- Create / append collections(stable) and readlists(experimental)
    - 'Smart' collections and readlists (Based on search parameters from the Komga API).
    - Orginize created / managed collections and readlists into groups with prefixs automaticly being added to its name.
    - Add custom poster art for collections and readlists.
    - Add an overlay to custom or default poster art based on its collection or readlist group.



### Still to be implemented
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
  Example Catagory : 'Ex Prefix: '

smart_collections : 

  - collection_name : Favorite Character
    collection_catagory : Example Catagory
    search_params : 
      search : <your favorite character's name>

  - collection_name : Second Favorite Character
    collection_catagory : Example Catagory
    search_params : 
      search : <your second favorite character's name>
```
    
- Run Kmm.py

<!-- See [docs](./docs/) for further usage examples. -->
