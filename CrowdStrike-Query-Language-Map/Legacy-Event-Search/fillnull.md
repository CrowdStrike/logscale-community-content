Comments: In Legacy Event Search, the function `fillnull` is used to populate blank fields with a default value. Example:

```
| fillnull value="N/A" GrandParentBaseFileName, ParentBaseFileName
```

in LogScale:

```
| default(value="N/A", field=[GrandParentBaseFileName, ParentBaseFileName])
```

[[default]]
