https://attack.mitre.org/techniques/T1201/

Windows

```
#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ event_platform=Win ((ImageFileName=/\\net1?\.exe/i CommandLine=/accounts/i) OR (/(Get-ADDefaultDomainPasswordPolicy|GetAccountPasswordPolicy)/i))
```

Linux/macOS

```
#event_simpleName=ProcessRollup2 event_platform=/^(Mac|Lin)$/ ((ImageFileName=/\/(pwpolicy|chage|show)/i) OR (/\/etc\/pam\.d\/common\-password/))
```