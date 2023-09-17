The `count` function counts the number of events in the repository, or streaming through the function. The result is put in a field named, `_count`. You can use this field name to pipe the results to other query functions or for general use.

It is possible to specify a field and only events containing that field are counted. It is also possible to output a distinct count. 

Count

```
| count(FileName, as=executionCount)
```

Distinct Count

```
| count(aid, distinct=true, as=uniqueEndpoints)
```

[count Documentation](https://library.humio.com/data-analysis/functions-count.html)
