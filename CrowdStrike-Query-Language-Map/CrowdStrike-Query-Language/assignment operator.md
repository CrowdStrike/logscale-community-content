The assignment operator (`:=`) sets the value of a specified field to a value or the result of a formula. You can use the operator `:=` with functions that take an `as` parameter.

```
| timeDeltaSeconds := (now()*1000)-ProcessStartTime
```

[Assignment Operator Documentation](https://library.humio.com/data-analysis/syntax-fields.html#syntax-fields-assignment-operator)