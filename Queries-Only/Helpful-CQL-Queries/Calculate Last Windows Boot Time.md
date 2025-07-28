
```
#event_simpleName=AgentOnline event_platform=Win  
| groupBy([aid], function=([selectLast([BaseTime])]))
| LastReboot_milli:=(BaseTime/1000*1024)+978307200
| round("LastReboot_milli")
| LastRebootAgo:=now()-(LastReboot_milli*1000)
| formatDuration("LastRebootAgo", precision=2)
| LastReboot:=formatTime(format="%F %T %Z", field="LastReboot_milli")
```