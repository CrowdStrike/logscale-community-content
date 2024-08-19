```
// Get all Windows ProcessRollup2 events with .dll or .exe listed in the call stack
event_platform=Win #event_simpleName=ProcessRollup2 CallStackModuleNames=/\.(dll|exe)/

// Create filters to narrow searches
| aid=?aid
| ComputerName=~wildcard(?{ComputerName="*"}, ignoreCase=true)
| UserName=~wildcard(?{UserName="*"}, ignoreCase=true)

// Clean up first few characters in CallStackModuleNames
| replace(field=CallStackModuleNames, regex="0\\<\\-1\\>", as=CallStackModuleNames)

// Remove memory addresses (optional)
| replace(field=CallStackModuleNames, regex="(\\.dll|\\.exe)\\+.*?\\|", with="$1|", as=CallStackModuleNames)

// Create arrary of module loads
| loadedFile:=splitString(by="\\|", field=CallStackModuleNames)

// Omit array values that are not exe or dll file paths
| array:filter(array="loadedFile[]", function={x=/\.(exe|dll)/i}, var=x)

// Concat results into unified field
| concatArray(field="loadedFile", as=CallStackModules, separator="|")

// Aggregate by process execution
| groupBy([cid, aid, TargetProcessId, ComputerName, UserName, UserSid, ParentBaseFileName, FileName, CommandLine], function=([collect([CallStackModules])]), limit=max)

// Put each CallStackModules value on its own line
| replace(field=CallStackModules, regex="\\|", with="\n", as=CallStackModules)

```