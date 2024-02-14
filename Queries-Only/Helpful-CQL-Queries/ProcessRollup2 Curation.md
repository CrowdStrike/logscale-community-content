```
// Specify data source and simpleName (index)
#event_simpleName=ProcessRollup2

// search for net.exe and net1.exe (including path, hence the wildcard)

| ImageFileName =~ in(values=["*\\cmd.exe", "*\\powershell.exe"])

// group data and summarize

| groupBy(["#cid", "aid", "UserSid", "ImageFileName", "CommandLine"], function=[count(as=executionCount), selectLast(["TargetProcessId"])])

// enrich sid -> username and aid -> ComputerName, not in the ProcessRollup event when through FDR

| join({#event_simpleName = "UserIdentity" | groupBy(["#cid", "aid", "UserSid"], function=selectLast(["UserName"]))}, include="UserName", field=["#cid", "aid", "UserSid"])
| join({#event_simpleName!=* EventType != "Event_ExternalApiEvent" | groupBy(["#cid", "aid"], function=selectLast(["ComputerName"]))}, include="ComputerName", field=["#cid", "aid"])

// Create RTR and PE links, Humio supports markdown!

| RTR := format("[RTR](https://falcon.eu-1.crowdstrike.com/activity/real-time-response/console/?start=hosts&aid=%s)",field=["aid"])
| "Process Explorer" := format("[Explore](https://falcon.eu-1.crowdstrike.com/investigate/process-explorer/%s/%s)", field=["aid", "TargetProcessId"])

// Split string to only get filename

| FileName := splitString(field="ImageFileName", by="\\\\", index="-1")

// Table the output!

| table(["aid", "ComputerName", "UserName", "FileName", "UserSid", "CommandLine", "executionCount", "TargetProcessId", "RTR", "Process Explorer"])

```