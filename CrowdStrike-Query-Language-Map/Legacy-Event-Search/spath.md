Comments: In Legacy Event Search, the function `spath` allows you to extract information from the structured data formats XML and JSON. Example for XML:

```
| spath output=dates path=purchases.book.title{@yearPublished} 
```

In LogScale, the functions `parseJson` and `parseXml` would be used as desired. 

```
| parseXml(purchases)
```

or, if the input was JSON formatted:

```
| parseJson(purchases)
```

[[parseXml]] | [[parseJson]]
