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

#### Version with user parameters (caution: you will need to include .* instead of * for a broader search to work, or simply leave the parameters empty):
```
#event_simpleName=ProcessRollup2
| aid=?aid
| regex(regex=?{ParentFile=".*"}, field=ImageFileName, flags="mi")
| ImageFileName=/(\/|\\)(?<FileName>\w*\.?\w*)$/
| join({
    #event_simpleName=ProcessRollup2
    | aid=?aid
    | regex(regex=?{ParentFile=".*"}, field=ParentBaseFileName, flags="mi")
    | regex(regex=?{ChildFile=".*"}, field=ImageFileName, flags="mi")
    | MD5 := MD5HashData
    | ImageFileName=/(\/|\\)(?<ChildFileName>\w*\.?\w*)$/
    | ChildCLI := CommandLine
    | ChildUser := UserName
  }, key=ParentProcessId, field=TargetProcessId, include=[MD5, ChildFileName, ChildCLI, ChildUser], limit=200000)
| groupBy([aid, ComputerName, UserName, ChildUser, FileName, CommandLine, ChildFileName, ChildCLI, MD5], limit=max)

```
