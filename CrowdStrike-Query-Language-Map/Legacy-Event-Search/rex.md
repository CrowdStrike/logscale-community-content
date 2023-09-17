Comments: In Legacy Event Search, the `rex` function is used to extract strings from fields using regular expressions. Example:

```
event_simpleName=ProcessRollup2 event_platform=Win
| rex field=ImageFileName "\\\Device\\\HarddiskVolume\d+(?<ShortFilePath>\\\.+\\\).+$"
| table FileName, ShortFilePath, ImageFileName
```

In LogScale, regular expression field extractions can be invoked in two ways. First, inline by encasing the regex in forward slashes (`\`). These regex statements are strict and non-matches will be discarded.

```
#event_simpleName=ProcessRollup2 event_platform=Win
| ImageFileName=/\\Device\\HarddiskVolume\d+(?<ShortFilePath>\\.+\\)(?<FileName>.+$)/
| select([FileName, ShortFilePath, ImageFileName])
```

The second is by invoking the `regex` function. These regex statements are strict by default, but that can be toggled.

```
#event_simpleName=ProcessRollup2 event_platform=Win
| regex("\\\Device\\\HarddiskVolume\d+(?<ShortFilePath>\\\.+\\\)(?<FileName>.+$)", field=ImageFileName, strict=false)
| select([FileName, ShortFilePath, ImageFileName])
```

Note that the parameter `strict` is set to `false` in the above example.

[[regex - extraction via capture]] | [[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/regex|regex]]

