Matches a value in the CSV or through a limited form of JSON file, uploaded using Lookup Files.

```
| match(file="fdr_aidmaster.csv", field=aid, include=ComputerName, ignoreCase=true, strict=false)
```

to output all columns of a lookup:

```
| aid =~ match(file="fdr_aidmaster.csv", column=aid, strict=false)
```

```
| cid =~ match(file="cid_name.csv", column=cid, strict=true)
```

[match Dcoumentation](https://library.humio.com/data-analysis/functions-match.html)
