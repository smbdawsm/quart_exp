# GTN STORAGE service

- app required Redis on localhost:6379 with low query
- app required MongoDB on localhost:27017

 - Application works at 5050 port
# API reference:

-  `/api/storage/add` 'GET' request, takes to input json like:


```
    {
        "user_id": "user1",
        "hash_id": "some3",
        "query": "some2",
        "result" : {"dictionary": 1 }
    }
 ```


-  `/api/storage/search` 'GET' request, takes to input json like:

```
    {
        "user_id": ...,
        "query": ....,
        "engine": .....,
        "date_from": ....
    }
```