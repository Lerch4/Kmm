# Readlist
- Readlists can be added through smart searching for books or series(expirimental) or by adding cbl files from a url or the assets folder.

### Readlist Parameters
```    
readlist_name: str # required
overlay_mode: 'no_asset'| 'force' | 'disable'

# For adding from cbl(will be used over search)
cbl: str| list[str] # file path or url
display_unmatched: bool

# For adding from search
readlist_category: str
series_search_params: list[dict]
book_search_params: list[dict]
readlist_prefix: str
book_ids: list[str]
series_ids: list[str]
blacklisted_book_ids: list[str]
blacklisted_book_search_params: dict | list[dict]
blacklisted_series_search_params: dict | listlist[dict]
ordered: bool
overwrite: bool
parent_readlist_ids: list[str]
parent_readlist_names: list[str]

```



 