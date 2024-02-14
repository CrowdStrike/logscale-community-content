```
aid=?aid #event_simpleName=ProcessRollup2 ImageFileName=/\\outlook.exe/i

| ImageFileName=/(\/|\\)(?<FileName>\w*\.?\w*)$/
| join( { #event_simpleName=ProcessRollup2 | ParentBaseFileName=/outlook.exe/i | ImageFileName=/(chrome|firefox|iexplore)\.exe/i | MD5 := MD5HashData | ImageFileName=/(\/|\\)(?<ChildFileName>\w*\.?\w*)$/ | ChildCLI := CommandLine }, key=ParentProcessId, field=TargetProcessId, include=[MD5, ChildFileName, ChildCLI] )
| groupBy([aid, FileName, CommandLine, ChildFileName, ChildCLI, MD5], limit=max)

```