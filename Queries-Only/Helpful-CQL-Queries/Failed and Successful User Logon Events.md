```
#event_simpleName=/UserLogon/
| case{
    #event_simpleName=UserLogon | SuccessLogonTime:=ContextTimeStamp;
    #event_simpleName=UserLogonFailed2 | FailedLogonTime:=ContextTimeStamp;
}
| groupBy([UserSid, UserName], function=([min(FailedLogonTime, as=FirstFailedLogon), max(FailedLogonTime, as=LastFailedLogon), max(SuccessLogonTime, as=LastSuccessfulLogin), count(SuccessLogonTime, as=TotalSuccessfulLogins), count(FailedLogonTime, as=TotalFailedLogins), selectFromMax(field="@timestamp", include=[PasswordLastSet]), {#event_simpleName=UserLogon | selectFromMax(field="@timestamp", include=[ComputerName]) | rename(field="ComputerName", as="LastLoggedOnHost")}]))
| TotalFailedLogins>3
| $falcon/helper:enrich(field=UserLogonFlags)
| formatTime(format="%F %T", field=FirstFailedLogon, as="FirstFailedLogon", timezone="EST")
| formatTime(format="%F %T", field=LastFailedLogon, as="LastFailedLogon", timezone="EST")
| formatTime(format="%F %T", field=LastSuccessfulLogin, as="LastSuccessfulLogin", timezone="EST")
| PasswordLastSet:=PasswordLastSet*1000 | formatTime(format="%F %T", field=PasswordLastSet, as="PasswordLastSet", timezone="EST")
| default(value="-", field=[FirstFailedLogon, LastFailedLogon, LastSuccessfulLogin, TotalSuccessfulLogins, TotalFailedLogins, PasswordLastSet, LastLoggedOnHost])
| sort(order=desc, TotalFailedLogins, limit=20000)
```