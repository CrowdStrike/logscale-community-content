https://attack.mitre.org/techniques/T1482/

Windows

```
#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ event_platform=Win ((ImageFileName=/\\nltest\.exe/i CommandLine=/trust/i) OR (ImageFileName=/\\dsquery\.exe/i CommandLine=/trustedDomain/i) OR (/(Get-NetDomainTrust|Get-NetForestTrust|Get-AcceptedDomain)/i))
```
