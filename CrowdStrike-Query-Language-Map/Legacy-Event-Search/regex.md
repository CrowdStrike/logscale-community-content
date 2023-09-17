Comments: In Legacy Event Search, the `regex` function is used to search fields leveraging regular expressions. Example:

```
event_simpleName=ProcessRollup2 event_platform=Win FileName IN (cmd.exe, powershell.exe)
|  regex CommandLine="\s+\-e(nc|ncodedCommand)\s+"
```

In LogScale:

```
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\(powershell|cmd)\.exe/i
| CommandLine=/\s+\-e(nc|ncodedCommand)\s+/i
```

Note: regular expressions can be used almost anywhere in LogScale by encasing the syntax in forward slashes (`/`). A wildcard is assumed at the beginning and the end of each search. Example:

```
| ImageFileName=/powershell/i
```

is the regex equivalent of:

```
| ImageFileName=/.*powershell.*/i
```

the `i` at the end removes case sensitivity.

[[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/regex|regex]]


