https://attack.mitre.org/techniques/T1082/

Windows

```
#event_simpleName=ProcessRollup2 event_platform=Win ((ImageFileName=/\\(fsutil|fsinfo|drives|systeminfo|vssadmin|hostname)\.exe/i) OR (ImageFileName=/\\net1?\.exe/i CommandLine=/config/i))
```

Linux/macOS

```
#event_simpleName=ProcessRollup2 event_platform=/^(Lin|Mac)$/ ImageFileName=/\/(systeminfo|systemsetup|df|uname|system_profiler|lsmod|csrutil|kmod|hostname)/
```

