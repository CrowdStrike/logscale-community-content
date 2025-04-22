```
// Create a live table of the executables in System32/SysWOW64
| defineTable(query={
    #event_simpleName=ProcessRollup2 event_platform=Win FilePath=/\\Windows\\(System32|SysWOW64)\\/ FileName=/\.exe$/
    | FilePath=/(\\Device\\HarddiskVolume\d+)?(?<ExpectedFilePath>\\.+)/
    | groupBy([FileName, ExpectedFilePath], function=[])
    }, 
    include=[FileName, ExpectedFilePath], name="LOLBinLocation", start=7d)
    
// Search for running executables not in System32/SysWOW64
| #event_simpleName=ProcessRollup2 event_platform=Win FilePath!=/\\Windows\\(System32|SysWOW64)\\/ FileName=/\.exe$/

// Look for when the name of a file running outside System32/SysWOW64 matches the file name of a binary in System32/SysWOW64
| match(file="LOLBinLocation", field=[FileName], include=[ExpectedFilePath], strict=true)

// Shorten file path
| FilePath=/(\\Device\\HarddiskVolume\d+)?(?<FilePath>\\.+)/

// Output to table
| table([@timestamp, aid, ComputerName, UserName, FileName, FilePath, ExpectedFilePath, CommandLine])
```