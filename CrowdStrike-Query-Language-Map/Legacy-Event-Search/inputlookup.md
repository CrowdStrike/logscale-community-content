Comments: In Legacy Event Search, the function `inputlookup` is used to read a lookup file. Example:

```
| inputlookup AsepClass.csv
```

in LogScale:

```
| readFile("falcon/investigate/AsepClass.csv")
```

[[readFile]]
