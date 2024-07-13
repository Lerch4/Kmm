# KomgaMetaManager (Kmm) 

Kmm is a script to help customize and organize your [Komga](https://komga.org/) server. It is loosly inspired by [Kometa (formerly Plex Meta Manager)](https://kometa.wiki/en/latest/). Kmm is still under development and has not been thoroughly tested. 

### Currently Kmm has the ability to
- Create / append collections(stable) and readlists(experimental)
    - 'Smart' collections and readlists (Based on search parameters from the Komga API).
    - Orginize created / managed collections and readlists into groups with prefixs automaticly being added to its name.
    - Add custom poster art for collections and readlists.
    - Add an overlay to custom or default poster art based on its collection or readlist group.
    - Add readlists from matched .cbl file
        - Add community .cbl lists from raw url (tested with https://github.com/DieselTech/CBL-ReadingLists)

### To be implemented
- [ ] Make readlists from other readlists
- [ ] Make readlist from multiple cbl files

- Long Term Goals
    - [ ] Add optional cashing for Komga data and community cbl files
    - [ ] Add / edit / scrape series metadata (series.json)
    - [ ] Add / edit / scrape book metadata (ComicInfo.xml)
    - [ ] Add scheduling



## **Installation**
- First Download and extract Kmm repo 
-  Then install requirements
    - `pip install -r requirements.txt`

## **Usage**
- Set up config directory and config.yml file
    - [Example config.yml](/EXAMPLE_config/config.yml)

- Run kmm.py
```
python kmm.py
```

<!-- See [docs](./docs/) for further usage examples. -->
