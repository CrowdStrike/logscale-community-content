https://attack.mitre.org/techniques/T1217/

Bookmark Discovery

```
#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ /bookmarks/i
| /(firefox|chrome|edge|iexplore)/i
```

Query Data Folder for Google Chrome

```
// Get events of interest for T1217
#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/

// Omit events where the browser is the executing process
| FileName!="chrome*"

// Normalize details field
| Details:=concat([CommandLine, CommandHistory,ScriptContent])

// Further narrow events with brute force search against Details field
| Details=/chrome/i

// Normalize Falcon UPID value
| falconPID:=TargetProcessId | falconPID:=ContextProcessId

// Check to see which operating system Chrome is being targeted on
| case {
Details=/\\AppData\\Local\\Google\\Chrome\\User\sData\\Default/i | BrowserTarget:="Windows - Google Chrome";
Details=/\/Users\/\S+\/Library\/Application\sSupport\/Google\/Chrome\/Default/i | BrowserTarget:="macOS - Google Chrome";
Details=/\/home\/\S+\/\.config\/google\-chrome\/Default/i | BrowserTarget:="Linux - Google Chrome";
}

// Check to see where targeting is found
| case {
#event_simpleName=ProcessRollup2 | Location:="Process Execution - Command Line";
#event_simpleName=CommandHistory | Location:="Process Execution - Command History";
#event_simpleName=/^ScriptControl/ | Location:="Script - Script Contents";
}

// Calculate hash for details field for use in groupBy statement
| DetailsHash:=hash(field=Details)

// Created shortened Details field of 100 characters to improve readability
| ShortDetails:=format("%,.100s", field=Details)

//Aggregate results
| groupBy([event_platform, BrowserTarget, Location, DetailsHash, ShortDetails], function=([count(aid, distinct=true, as=UniqueEndpoints), count(aid, as=ExecutionCount), selectFromMax(field="@timestamp", include=[aid, falconPID])]))

// Set threshold to look for results that have occured on fewer than 50 unique endpoints; adjust up or down as desired
| test(UniqueEndpoints<50)

// Add link to Graph Explorer
| format("[Last Execution](https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:%s:%s)", field=["aid", "falconPID"], as="Graph Explorer")

// Drop unneeded fields
| drop([aid, DetailsHash, falconPID])
```