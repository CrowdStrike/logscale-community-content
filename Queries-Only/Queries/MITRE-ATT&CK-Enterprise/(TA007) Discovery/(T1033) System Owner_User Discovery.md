https://attack.mitre.org/techniques/T1033/

All

```
#event_simpleName=ProcessRollup2 ((ImageFileName=/(\\|\/)(w|who|whoami)(\.exe)?$/i) OR (event_platform=Mac ImageFileName=/\/dscl/i CommandLine=/users/i))
```
