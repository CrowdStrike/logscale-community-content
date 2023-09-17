https://attack.mitre.org/techniques/T1652/

Windows

```
(#event_simpleName=ProcessRollup2 event_platform=Win (ImageFileName=/\\driverquery\.exe/i OR (ImageFileName=/\\sc\.exe/i CommandLine=/query/i))) OR (#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ event_platform=Win /CurrentControlSet\\(Services|HardwareProfiles)/)
```

Linux/macOS

```
#event_simpleName=ProcessRollup2 event_platform=/^(Lin|Mac)$/ ImageFileName=/\/(lsmod|modinfo)/i
```
