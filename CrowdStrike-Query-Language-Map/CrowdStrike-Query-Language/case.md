Using `case` expressions, you can describe alternative flows in your queries. It is similar to `case` or `cond` you might know from many other functional programming languages. It essentially allows you to write `if-then-else` constructs that work on events streams.

Destructive Case Statement

```
| case {
	UserIsAdmin=1 | UserIsAdmin := "True" ;
	UserIsAdmin=0 | UserIsAdmin := "False" ;
	*; 
}
```

Non-Destructive Case Statement

```
| case {
	UserIsAdmin=1 | _UserIsAdmin := "True" ;
	UserIsAdmin=0 | _UserIsAdmin := "False" ;
	*; 
}
```
 
[case Documentation](https://library.humio.com/data-analysis/syntax-conditional.html#syntax-conditional-case)
