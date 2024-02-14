```
#event_simpleName=UserLogon UserSid=S-1-5-21-*
| in(LogonType, values=["2","10"])
| ipLocation(aip)
| case {UserIsAdmin = "1" | UserIsAdmin := "Yes" ;
        UserIsAdmin = "0" | UserIsAdmin := "No" ;
        * }
| case {

        LogonType = "2" | LogonType := "Interactive" ;
        LogonType = "3" | LogonType := "Network" ;
        LogonType = "4" | LogonType := "Batch" ;
        LogonType = "5" | LogonType := "Service" ;
        LogonType = "7" | LogonType := "Unlock" ;
        LogonType = "8" | LogonType := "Network Cleartext" ;
        LogonType = "9" | LogonType := "New Credentials" ;
        LogonType = "10" | LogonType := "Remote Interactive" ;
        LogonType = "11" | LogonType := "Cached Interactive" ;
        * }
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
| case {UserIsAdmin = "1" | UserIsAdmin := "True" ;

        UserIsAdmin = "0" | UserIsAdmin := "False" ;
        * }
| case {
        LogonType = "2" | LogonType := "Interactive" ;
        LogonType = "3" | LogonType := "Network" ;
        LogonType = "4" | LogonType := "Batch" ;
        LogonType = "5" | LogonType := "Service" ;
        LogonType = "7" | LogonType := "Unlock" ;
        LogonType = "8" | LogonType := "Network Cleartext" ;
        LogonType = "9" | LogonType := "New Credentials" ;
        LogonType = "10" | LogonType := "Remote Interactive" ;
        LogonType = "11" | LogonType := "Cached Interactive" ;
        * }
| case {RemoteAccount = "0" | RemoteAccount := "Local" ;
        RemoteAccount = "1" | RemoteAccount := "Remote" ;
        * }
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