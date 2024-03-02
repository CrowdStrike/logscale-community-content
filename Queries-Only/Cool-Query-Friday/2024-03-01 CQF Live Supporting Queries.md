**CHEAT SHEET**

Link: https://github.com/CrowdStrike/logscale-community-content

**DEDUP**

EXAMPLE

```
FileName=testfile* | dedup ComputerName | stats count by ComputerName FileName FilePath
```

FINISHED

```
#event_simpleName=/FileWritten$/ FileName=/doc/i
| FilePath=/\\Device\\HarddiskVolume\d+(?<ShortFilePath>.+$)/
| groupBy([ComputerName, FileName, ShortFilePath])
```


**ADDING LINES TO OUTPUT**

```
#event_simpleName=ProcessRollup2\
| top([FileName], limit=10)
```



**DUPLICATE MACHINES**

Example: 

```
event_simpleName=AgentOnline
| stats dc(aid) AS aidCount by ComputerName
| where aidCount > 1
| sort - aidCount
| rename ComputerName AS "Endpoint", aidCount AS "AID Count"
```


FINSHIED

```
#event_simpleName=AgentOnline ComputerName!=""
| groupBy([ComputerName], function=([count(aid, distinct=true, as=aidCount), {selectFromMax(field="@timestamp", include=[aid, @timestamp]) | rename(field="aid", as="Latest AID")}, collect([aid])]))
| test(aidCount>1)
| rename([[ComputerName, Endpoint], [aidCount, "AID Count"], [@timestamp, "Time Read"]])
| "Time Read":=formatTime(format="%c", field="Time Read", timezone="EST")
```


**USERLOGON FAILED**

```
event_platform=win event_simpleName=UserLogonFailed2 
| eval SubStatus_hex=tostring(SubStatus_decimal,"hex")
| rename SubStatus_decimal as Status_code_decimal
| lookup local=true LogonType.csv LogonType_decimal OUTPUT LogonType
| lookup local=true win_status_codes.csv Status_code_decimal OUTPUT Description 
| stats count(aid) as failCount earliest(ContextTimeStamp_decimal) as firstLogonAttempt latest(ContextTimeStamp_decimal) as lastLogonAttempt values(LocalAddressIP4) as localIP values(aip) as externalIP by aid, ComputerName, UserName, LogonType, SubStatus_hex, Description 
| eval firstLastDeltaHours=round((lastLogonAttempt-firstLogonAttempt)/60/60,2)
| eval logonAttemptsPerHour=round(failCount/firstLastDeltaHours,0)
| convert ctime(firstLogonAttempt) ctime(lastLogonAttempt)
| sort - failCount
```

FINSIHED

```
#event_simpleName=UserLogonFailed2 event_platform=Win
| SubStatus_hex := format(field=SubStatus, "0x%x")
| $falcon/helper:enrich(field=SubStatus)
| $falcon/helper:enrich(field=LogonType)
| groupBy([aid, ComputerName, UserName, LogonType, SubStatus_hex, SubStatus], function=([count(aid, as=failCount), min(ContextTimeStamp, as=firstLogonAttempt), max(ContextTimeStamp, as=lastLogonAttempt), collect([LocalAddressIP4, aip])]))
| failCount>50
| firstLastDeltaHours:=(lastLogonAttempt-firstLogonAttempt)/60/60 | firstLastDeltaHours:=round("firstLastDeltaHours")
| logonAttemptsPerHour:=(failCount/firstLastDeltaHours) | logonAttemptsPerHour:=round("logonAttemptsPerHour")
| firstLogonAttempt:=formatTime(format="%F %T.%L %Z", field="firstLogonAttempt")
| lastLogonAttempt:=formatTime(format="%F %T.%L %Z", field="lastLogonAttempt")
| sort(failCount, order=desc, limit=20000)
```



**MULTIPLE USER LOGINS**


```
#event_simpleName=UserLogon
| UserName=username
// exclude computers (systems end with $)
| UserName!=/\w+\$$/
// exclude SYSTEM account
| UserSid!=S-1-5-18
//exclude LOCAL SERVICE accounts
| UserName!="LOCAL SERVICE"
// enrich with logontype & userisadmin data
| $falcon/helper:enrich(field=LogonType)
| $falcon/helper:enrich(field=UserIsAdmin)
//exclude batch logon type
| LogonType!=Batch
| groupBy([UserName, ComputerName, LogonType, UserIsAdmin])
```


MULTIPLE DONE

```
#event_simpleName=UserLogon
| in(field="UserName", values=[Administrator, sean1])
// exclude computers (systems end with $)
| UserName!=/\w+\$$/
// exclude SYSTEM account
| UserSid!=S-1-5-18
//exclude LOCAL SERVICE accounts
| UserName!="LOCAL SERVICE"
// enrich with logontype & userisadmin data
| $falcon/helper:enrich(field=LogonType)
| $falcon/helper:enrich(field=UserIsAdmin)
//exclude batch logon type
| LogonType!=Batch
| groupBy([UserName, ComputerName, LogonType, UserIsAdmin])
```


BASELINE

```
#event_simpleName=UserLogon
| in(field="UserName", values=[Administrator, sean1, demo])
| LogonTime:=LogonTime*1000
| TimeBucket:=formatTime(format="%F %H", field="LogonTime")
| groupBy([TimeBucket, UserName])
```