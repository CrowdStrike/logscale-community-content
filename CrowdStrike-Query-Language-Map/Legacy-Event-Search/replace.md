Comments: In Legacy Event Search, the function `replace` is used to substitute strings or values within a field. Example:

```
event_simpleName=ProcessRollup2
| replace S-1-5-18 WITH SYSTEM IN UserSid_readable
```

In LogScale

```
#event_simpleName=ProcessRollup2
| replace("S-1-5-18", with="SYSTEM", field=UserSid)
```

Note: in LogScale, the `replace` search can accept regex and perform extractions and field substitutions. Example:

```
#event_simpleName=ProcessRollup2 event_platform=Win
| replace("^(\\\Device\\\HarddiskVolume\d+)", with="C:", field=ImageFileName, as=b)
```

[[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/replace|replace]]

