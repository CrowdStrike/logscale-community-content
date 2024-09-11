Accounts for when events do not contain all hour/day permutations:

```
#event_simpleName=UserLogon \\UserName="demo"
| UserName=~wildcard(?{UserName="*"}, ignoreCase=true)
| LogonTime:=LogonTime*1000
| time:dayOfWeekName(LogonTime)
| bucket(span=1h, field=[_hour,_dayOfWeekName])
| time:dayOfWeekName(_bucket)
| time:hour(_bucket)
| groupby([_hour,_dayOfWeekName], function=sum(_count, as="count"))
| case{
    _dayOfWeekName="Monday"    | _dayOfWeekName:="1-Mon";
    _dayOfWeekName="Tuesday"   | _dayOfWeekName:="2-Tu"; 
    _dayOfWeekName="Wednesday" | _dayOfWeekName:="3-Wed";
    _dayOfWeekName="Thursday"  | _dayOfWeekName:="4-Thur"; 
    _dayOfWeekName="Friday"    | _dayOfWeekName:="5-Fri";
    _dayOfWeekName="Saturday"  | _dayOfWeekName:="6-Sat"; 
    _dayOfWeekName="Sunday"    | _dayOfWeekName:="7-Sun"; 
}
| sort(field=_hour, reverse=false)
| sort(field=_dayOfWeekName, reverse=false)
```