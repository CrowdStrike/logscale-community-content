```
// Get all Windows ProcessRollup2 Events
#event_simpleName=ProcessRollup2 event_platform=Win
// Narrow to processes of interest and create FileName variable
| ImageFileName=/\\(?<FileName>(whoami|net1?|systeminfo|ping|nltest|sc|hostname|ipconfig)\.exe)/i
// Get timestamp value with date and hour value
| ProcessStartTime := ProcessStartTime*1000
| dayBucket := formatTime("%Y-%m-%d %H", field=ProcessStartTime, locale=en_US, timezone=Z)
// Force CommandLine and FileName into lower case
| CommandLine := lower(CommandLine)
| FileName := lower(FileName)
// Parse flag used in "net" command
| regex("(sc|net1?)\s+(?<netFlag>\S+)\s+", field=CommandLine, strict=false)
// Force netFlag to lower case
| netFlag := lower(netFlag)
// Create evaulation criteria and weighting for process usage; modified behaviorWeight integer as desired
| case {
       FileName=/net1?\.exe/ AND netFlag="start" | behaviorWeight := "4" ;
       FileName=/net1?\.exe/ AND netFlag="stop" | behaviorWeight := "4" ;
       FileName=/net1?\.exe/ AND netFlag="stop" AND CommandLine=/falcon/i | behaviorWeight := "25" ;
       FileName=/sc\.exe/ AND netFlag="start" | behaviorWeight := "4" ;
       FileName=/sc\.exe/ AND netFlag="stop" | behaviorWeight := "4" ;
       FileName=/sc\.exe/ AND netFlag=/(query|stop)/i AND CommandLine=/csagent/i | behaviorWeight := "25" ;
       FileName=/net1?\.exe/ AND netFlag="share" | behaviorWeight := "2" ;
       FileName=/net1?\.exe/ AND netFlag="user" AND CommandLine=/\/delete/i | behaviorWeight := "10" ;
       FileName=/net1?\.exe/ AND netFlag="user" AND CommandLine=/\/add/i | behaviorWeight := "10" ;
       FileName=/net1?\.exe/ AND netFlag="group" AND CommandLine=/\/domain\s+/i | behaviorWeight := "5" ;
       FileName=/net1?\.exe/ AND netFlag="group" AND CommandLine=/admin/i | behaviorWeight := "5" ;
       FileName=/net1?\.exe/ AND netFlag="localgroup" AND CommandLine=/\/add/i | behaviorWeight := "10" ;
       FileName=/net1?\.exe/ AND netFlag="localgroup" AND CommandLine=/\/delete/i | behaviorWeight := "10" ;
       FileName=/nltest\.exe/ | behaviorWeight := "3" ;
       FileName=/systeminfo\.exe/ | behaviorWeight := "3" ;
       FileName=/whoami\.exe/ | behaviorWeight := "3" ;
       FileName=/ping\.exe/ | behaviorWeight := "3" ;
       FileName=/hostname\.exe/ | behaviorWeight := "3" ;
       FileName=/ipconfig\.exe/ | behaviorWeight := "3" ;
 * }
| default(field=behaviorWeight, value=1)
// Create FileName and CommandLine one-liner
| format(format="(Score: %s) %s • %s", field=[behaviorWeight, FileName, CommandLine], as="executionDetails")
// Group and organize output
| groupby([cid,aid, dayBucket], function=[count(FileName, distinct=true, as="fileCount"), sum(behaviorWeight, as="behaviorWeight"), series(executionDetails)], limit=max)
// Set thresholds
| fileCount >= 5 OR behaviorWeight > 30
// Add Host Search link
| format("[Host Search](https://falcon.crowdstrike.com/investigate/events/en-us/app/eam2/investigate__computer?earliest=-24h&latest=now&computer=*&aid_tok=%s&customer_tok=*)", field=["aid"], as="Host Search")
// Sort descending by behavior weighting
| sort(behaviorWeight)
| drop([@timestamp, _duration])

```

[[regex]] | [[regex - extraction]] | [[lower]] | [[case]] | [[default]] | [[format - concat]] | [[groupBy]] | [[format - hyperlinks]] | [[sort]] | [[drop]] 