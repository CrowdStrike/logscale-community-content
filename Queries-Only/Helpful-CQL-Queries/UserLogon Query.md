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
| LogonTime := LogonTime*1000
| PasswordLastSet := formatTime("%Y-%m-%d %H:%M:%S", field=PasswordLastSet, locale=en_US, timezone=Z)
| LogonTime := formatTime("%Y-%m-%d %H:%M:%S", field=LogonTime, locale=en_US, timezone=Z)
| table(["LogonTime", "aid", "UserName", "UserSid", "LogonType", "UserIsAdmin", "PasswordLastSet", "aip.city", "aip.state", "aip.country"])
```