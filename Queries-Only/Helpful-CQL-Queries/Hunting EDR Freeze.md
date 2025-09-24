Based on the default command line switching behavior found in the [EDR-Freeze](https://github.com/TwoSevenOneT/EDR-Freeze?tab=readme-ov-file) open source project:

```
// Look for process handles opening Falcon
#event_simpleName=FalconProcessHandleOpDetectInfo FileName="WerFaultSecure.exe"

// Check for command line switching signal
| GrandparentCommandLine=/\.exe"?\s+\d+\s+\d+$/ OR ParentCommandLine=/\.exe"?\s+\d+\s+\d+$/ OR CommandLine=/\.exe"?\s+\d+\s+\d+$/

// Create process lineage tree for easier reading
| ProcessLineage:=format(format="%s (%s)\n\t└ %s (%s)\n\t\t└ %s (%s)", field=[GrandparentImageFileName, GrandparentCommandLine, ParentImageFileName, ParentCommandLine, ImageFileName, CommandLine])

// Output deatils to table
| table([@timestamp, aid, ComputerName, ContextProcessId, ProcessLineage])

// Create direct link to Process Explorer - Uncomment the rootURL value that matches your cloud
| rootURL  := "https://falcon.crowdstrike.com/" /* US-1 */
//| rootURL  := "https://falcon.us-2.crowdstrike.com/" /* US-2 */
//| rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/" /* Gov */
//| rootURL  := "https://falcon.eu-1.crowdstrike.com/"  /* EU */
| format("[Responsible Process](%sgraphs/process-explorer/tree?id=pid:%s:%s)", field=["rootURL", "aid", "ContextProcessId"], as="Process Explorer") 

// Remove unnecessary fields
| drop([rootURL, ContextProcessId])
```