Comments: The `eval` function is leveraged when you wish to create, convert, or analyze field values in Legacy Event Search and it serves many purposes. The most common are below:

##### 1. Create a new field that contains the result of a calculation

`... | eval speed=distance/time`

in LogScale:

```
| speed := distance/time
```

[[assignment operator]]

##### 2. Use the if function to analyze field values

`... | eval error = if(status == 200, "OK", "Problem")`

in LogScale:

```
| status match {
	200 => error := "OK" ;
	* => error := "Problem" ;
}
```

[[match]]

##### 3. Convert values to lowercase

`... | eval lowuser = lower(username)`

in LogScale:

```
| lowuser := lower(username)
```

[[lower]]

##### 4. Return a string value based on the value of a field

`... | eval error_msg = case(error == 404, "Not found", error == 500, "Internal Server Error", error == 200, "OK")`

in LogScale:

```
| case {
	error=404 | error_msg:="Not found";
	error=500 | error_msg:="Internal Server Error";
	error=200 | error_msg:="OK";
	*;
}
```

[[case]]

##### 5. Concatenate values from two fields

`... | eval full_name = first_name+" "+last_name`

in LogScale:

```
| format(format="%s %s", field=[first_name, last_name], as=full_name)
```

[[format - concat]]

##### 6. Separate multiple eval operations with a comma

`... | eval full_name = last_name+", "+first_name, low_name = lower(full_name)`

in LogScale:

```
| format(format="%s %s", field=[first_name, last_name], as=full_name)
| full_name:=lower(full_name)
```

[[format - concat]] | [[assignment operator]] | [[lower]]

##### 7. Convert a numeric field value to a string and include commas in the output

`... | eval x=tostring(x, "commas")`

in LogScale:

```
| x := format(field=x, "%s")
```

[[assignment operator]] | [[format - field conversions]]

##### 8. Include a currency symbol when you convert a numeric field value to a string

`... | eval x="$"+tostring(x, "commas")`

in LogScale:

```
| x := format(field=x, "$%s")
```

[[format - field conversions]]

##### 9. Calculate the length of a string

```
event_simpleName=ProcessRollup2 
| eval cmdLength=len(CommandLine)
| stats count by cmdLength, CommandLine
```

in LogScale:

```
#event_simpleName=ProcessRollup2 
| cmdLength:=length("CommandLine")
| groupBy([cmdLength, CommandLine])
```

[[length]]

##### 10. Round numbers

```
| eval totalMB = round(kb/1024,0)
```

in LogScale:

```
| totalMB := kb/1024
| totalMB := round(totalMB)
```

With decimal point precision:

```
| eval totalMB = round(kb/1024,2)
```

in LogScale:

```
| totalMB := kb/1024
| totalMB := format("%,.2f",field=["totalMB"])
```

[[round]] | [[format - rounding numbers]]

##### 11. Convert field in seconds to a time duration

```
| eval tostring(timeDelta,"duration")
```

in LogScale:

```
| formatDuration(timeDelta, as=timeDeltaFormatted)
```

[[formatDuration]]