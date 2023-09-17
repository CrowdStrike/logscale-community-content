```
// Get ReflectiveDotnetModuleLoad with non-null ManagedPdbBuildPath field.
#event_simpleName=ReflectiveDotnetModuleLoad event_platform=Win ManagedPdbBuildPath!=""

// Capture FilePath and FileName Fields
| ImageFileName=/(\\Device\\HarddiskVolume\d+)?(?<FilePath>.+\\)(?<FileName>.+)/

// Exclude things in Windows and Program Files folders
| FilePath!=/^\\(Windows|Program\sFiles|Program\sFiles\s\(x86\))\\/

// Aggregate results by FileName and FilePath
| groupBy([FileName, FilePath], function=([count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=executionCount), count(ManagedPdbBuildPath, distinct=true, as=uniqueManagedPdbBuildPath), collect([AssemblyName, ManagedPdbBuildPath]), selectFromMax(field="@timestamp", include=[aid, ContextProcessId])]))

// Create thresholds for conditions
| test(uniqueEndpoints<5)
| test(uniqueManagedPdbBuildPath<10)
| test(executionCount<100) 

// Remove unwanted files that slip through filter
| !in(field="FileName", values=["Docker Desktop Installer.exe"])

// Add Graph Explorer
| rootURL := "https://falcon.crowdstrike.com/" /* US-1 */
//| rootURL := "https://falcon.us-2.crowdstrike.com/" /* US-2 */
//| rootURL := "https://falcon.laggar.gcw.crowdstrike.com/" /* Gov */
//| rootURL := "https://falcon.eu-1.crowdstrike.com/" /* EU */
| format("[Graph Explorer](%sgraphs/process-explorer/graph?id=pid:%s:%s)", field=["rootURL", "aid", "ContextProcessId"], as="Last Execution")

// Drop unnecessary fields
| drop([rootURL, aid, ContextProcessId])
```