```
#event_simpleName=ProcessRollup2

| ImageFileName=/(\\|\/)(?<fileName>whoami+(\.exe)?$)/i
| concat([UID, UserSid], as="userIdentifier")
| format(format="%s > %s > %s { %s }", field=[GrandParentBaseFileName, ParentBaseFileName, fileName, CommandLine], as="processLineage")
| bucket(60min, field=[aid], function=stats([collect([processLineage]), count(field=userIdentifier, as="uidCount", distinct=true), count(aid, as="whoamiCount")]))
| whoamiCount > 1
| formattime("%A %d %B %Y, %R", as=_bucket, field=_bucket, timezone=EST)

```