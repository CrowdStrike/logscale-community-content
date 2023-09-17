Comments: In Legacy Event Search, the `where` function is used to compare the values of one or more fields. Example:

```
... | where distance/time > 100
```

In LogScale:

```
| speed := distnace/time
| test(speed > 100)
```

[[assignment operator]] | [[test]]
