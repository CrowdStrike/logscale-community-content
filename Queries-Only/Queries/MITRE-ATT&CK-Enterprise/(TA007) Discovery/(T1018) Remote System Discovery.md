https://attack.mitre.org/techniques/T1018/

Windows

```
#event_simpleName=ProcessRollup2 event_platform=Win ((ImageFileName=/\\(ping|tracert)\.exe/i) OR (ImageFileName=/\\net1?\.exe/i CommandLine=/view/i) OR (ImageFileName=/\\nltest\.exe/i CommandLine=/\/dclist/i) OR (/\\etc\\hosts\\/i))
```

Linux/macOS

```
#event_simpleName=ProcessRollup2 event_platform=/^(Lin|Mac)$/ CommandLine=/\/etc\/hosts/i
```