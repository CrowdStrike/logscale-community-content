```
#event_simpleName=OsVersionInfo event_platform=Lin
| OSVersionFileData=*
| replace("([0-9A-Fa-f]{2})", with="%$1", field=OSVersionFileData, as=OSVersionFileData)
| OSVersionFileData:=urlDecode("OSVersionFileData")
| regex("PRETTY_NAME=\"(?<DistroName>[^\"]+)\"", field=OSVersionFileData, strict=false)
| match(file="fdr_aidmaster.csv", field=aid, include=ComputerName, ignoreCase=true, strict=false)
| groupBy(aid, function=([selectLast([ComputerName, DistroName, DistroVersion, AgentVersion])]))

```

OR

```
#event_simpleName=OsVersionInfo event_platform=Lin

| OSVersionString = /^Linux\s(?<hostName>\S+)\s(?<kernelVersion>\S+)\s/i
| OSVersionFileData=*
| replace("([0-9A-Fa-f]{2})", with="%$1", field=OSVersionFileData, as=OSVersionFileData)
| OSVersionFileData:=urlDecode("OSVersionFileData")
| regex("PRETTY_NAME=\"(?<DistroName>[^\"]+)\"", field=OSVersionFileData, strict=false)
| groupBy(aid, function=([selectLast([hostName, kernelVersion, AgentVersion, OSVersionFileData])]))

```

OR

```
#event_simpleName=OsVersionInfo event_platform=Mac

| OSVersionFileData=*
| replace("([0-9A-Fa-f]{2})", with="%$1", field=OSVersionFileData, as=OSVersionFileData)
| OSVersionFileData:=urlDecode("OSVersionFileData")
| replace("^<!DOCTYPE.*?>$", field=OSVersionFileData)
| parseXml(OSVersionFileData)
| format(format="%s %s (%s)", field=[plist.dict.string[2], plist.dict.string[3], plist.dict.string], as=ProductBuild)
| groupBy([aid], function=selectLast([OsVersionString, ProductBuild, AgentVersion, RFMState]))
| RFMState match {

    1 => RFMState := "RFM";
    0 => RFMState := "OK";
}
```