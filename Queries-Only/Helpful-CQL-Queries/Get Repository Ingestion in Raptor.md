Step 1 find which repo you'd like:

```
| top([#repo, #Vendor, #type])
```

Step 2 - enter in at least one of: repo, type, or Vendor from previous step into the dashboard params from this query:

```
#repo=?repo #type=?type #Vendor=?Vendor
| eventSize()
| unit:convert(_eventSize, to="G")
| sum("_eventSize")
```

