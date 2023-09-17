```
#event_simpleName=OsVersionInfo
| field_temp:= ?{ComputerName="*"}
| case {
	field_temp != /^\*$/ | regex(field=field_temp,regex = "(?<field_matched>.*?)(,|$)", repeat="true") | test(ComputerName==field_matched) | drop([field_matched,field_temp]) ;
	field_temp = /\*$/ | ComputerName=* | drop([field_temp]) ;
}
```

List must be comma delineated without a space. Example:

```
NO-FALCON,FALCONIDPTERM02
```
