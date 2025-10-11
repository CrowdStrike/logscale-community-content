```
aid=?aid #event_simpleName=ProcessRollup2 ImageFileName=/\\outlook.exe/i
| ImageFileName=/(\/|\\)(?<FileName>\w*\.?\w*)$/
| join( {
  aid=?aid
  | #event_simpleName=ProcessRollup2
  | ParentBaseFileName=/outlook.exe/i
  | ImageFileName=/(chrome|firefox|iexplore)\.exe/i
  | MD5 := MD5HashData
  | ImageFileName=/(\/|\\)(?<ChildFileName>\w*\.?\w*)$/
  | ChildCLI := CommandLine
  }, key=ParentProcessId, field=TargetProcessId, include=[MD5, ChildFileName, ChildCLI])
| groupBy([aid, FileName, CommandLine, ChildFileName, ChildCLI, MD5], limit=max)
```

#### Version with wildcard parameters
```
#event_simpleName=ProcessRollup2
| aid=?{aid=*}
| ImageFileName =~ wildcard(?{ImageFileName="*"}, ignoreCase=true, includeEverythingOnAsterisk=true)
| ImageFileName=/(\/|\\)(?<FileName>\w*\.?\w*)$/
| join({
    #event_simpleName=ProcessRollup2
    | aid=?{aid=*}
    | ParentBaseFileName =~ wildcard(?{ParentBaseFileName="*"}, ignoreCase=true)
    | ImageFileName =~ wildcard(?{ImageFileName="*"}, ignoreCase=true)
    | MD5 := MD5HashData
    | ImageFileName=/(\/|\\)(?<ChildFileName>\w*\.?\w*)$/
    | ChildCLI := CommandLine
    | ChildUser := UserName
  }, key=ParentProcessId, field=TargetProcessId, include=[MD5, ChildFileName, ChildCLI, ChildUser], limit=200000)
| groupBy([aid, ComputerName, UserName, ChildUser, FileName, CommandLine, ChildFileName, ChildCLI, MD5], limit=max)
```
