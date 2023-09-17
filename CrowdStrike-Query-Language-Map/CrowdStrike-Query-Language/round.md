The `round` function rounds a numeric input field to the nearest integer, with an optional method to set the rounding type.

```
| roundNumber:=round(number)
```

Example:

```
createEvents(["Number=1.2", "Number=1.23", "Number=1.234","Number=1.2345","Number=1.789"])
| kvParse()
| roundNumber:=round(Number)
| select([Number, roundNumber])
```

Please note that `round` will convert to the nearest whole integer. To round numbers with decimal-point precision, use `format`.

[round Documentation](https://library.humio.com/data-analysis/functions-round.html) | [round Examples](https://library.humio.com/data-analysis/functions-round.html#functions-round-examples) | [[format - rounding numbers]]

