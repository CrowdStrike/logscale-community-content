The `parseJason` function parses data as JSON. Specify `field=@rawstring` to parse the rawstring into JSON. It is possible to prefix the names of the extracted fields using the prefix parameter.

```
| replace(regex="\"SHA1HashData\":\"0000000000000000000000000000000000000000\",", with="", field=@rawstring, as=@rawstring)
| parseJson(@rawstring)
```

[parseJson Documentation](https://library.humio.com/data-analysis/functions-parsejson.html)
