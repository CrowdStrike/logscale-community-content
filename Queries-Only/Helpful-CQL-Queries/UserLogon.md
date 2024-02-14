```
#event_simpleName=UserLogon UserSid=S-1-5-21-*
| in(LogonType, values=["2","10"])
| ipLocation(aip)
| $falcon/helper:enrich(field=UserIsAdmin)
| $falcon/helper:enrich(field=UserLogon)
| PasswordLastSet := PasswordLastSet*1000
| ContextTimeStamp := ContextTimeStamp*1000
| PasswordLastSet := formatTime("%Y-%m-%d %H:%M:%S", field=PasswordLastSet, locale=en_US, timezone=Z)
| ContextTimeStamp := formatTime("%Y-%m-%d %H:%M:%S", field=ContextTimeStamp, locale=en_US, timezone=Z)
| table(["ContextTimeStamp", "aid", "UserName", "UserSid", "LogonType", "UserIsAdmin", "PasswordLastSet", "aip.city", "aip.state", "aip.country"])
```

```
#event_simpleName="UserLogon"
| UserSid=S-1-5-21-*
| table(["@timestamp", "ClientComputerName", "UserName", "UserIsAdmin", "RemoteAccount", "LogonType", "AuthenticationPackage", "UserSid"])
| $falcon/helper:enrich(field=UserIsAdmin)
| $falcon/helper:enrich(field=UserLogon)
```

```
#event_simpleName=UserLogon event_platform=Win
| groupBy(["#cid", "UserSid", "UserName", "LogonType", "LogonDomain"], function=[count(as=loginCount), selectLast(["@timestamp"])])

```

```
#event_simpleName=UserLogon
| UserSid=S-1-5-21-*
| ipLocation(field=aip)
| sankey(source="UserName",target="aip.country", weight=count(UserName))
```

```
#event_simpleName=UserLogon UserSid=S-1-5-21-* LogonType=10
| ipLocation(field=aip)
| worldMap(lat=aip.lat, lon=aip.lon, magnitude=count(aid))

```