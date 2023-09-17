Using `match` expressions, you can describe alternative flows in your queries where the conditions all check the same field. It is similar to the `switch` operation you might recognize from many other programming languages. It essentially enables you to write `if-then-else` constructs that work on events streams.

Destructive

``` 
| UserIsAdmin match {
	1 => UserIsAdmin := "True" ;
	0 => UserIsAdmin := "False" ;
}
```

Non-Destructive

```
| UserIsAdmin match {
	1 => _UserIsAdmin := "True" ;
	0 => _UserIsAdmin := "False" ;
}
```

[match Documentation](https://library.humio.com/data-analysis/syntax-conditional.html#syntax-conditional-match)
