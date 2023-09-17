Comments: In Legacy Event Search, the function `makeresults` is most commonly used to generate test data. Example:

```
| makeresults count=3 
| streamstats count
| eval shape = case(count=1, "Square", count=2, "Circle", count=3, "Triangle")
| eval color = case(count=1, "Red", count=2, "Blue", count=3, "Green")
```

In LogScale, a combination of `createEvents` and `kvParse` can be used. Example:

```
createEvents(["Shape=Square, Color=Red", "Shape=Circle, Color=Blue", "Shape=Triangle, Color=Green"])
| kvParse()
```

[[createEvents]] | [[kvParse]]
