# Collections
- Collections can be added through smart searching for series through paremeters given by the Komga api. Collections can also be added by providing a list series ids or other collection ids.

### Collection Parameters
```    
collection_name: str # required
collection_category: list[dict]
search_params: list[dict]
collection_prefix: str
series_ids: list[str]
blacklisted_series_ids: list[str]
blacklisted_search_params: dict | listlist[dict]
parent_collection_ids: list[str]
parent_collection_names: list[str]
ordered: bool
overwrite: bool
overlay_mode: 'no_asset'| 'force' | 'disable'
```

