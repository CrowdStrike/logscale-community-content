The `correlate()` function looks for patterns across given search parameters.

In the example below, correlate looks for the commands whoami, net, and systeminfo  being run on the same system within a 5 minute time interval. The `sequence` parameter is set to `false` indicating that the ordering of the events does not matter.

```
correlate(
    // Search for whoami executions on Windows
    whoami: {
         #event_simpleName=ProcessRollup2 event_platform=Win FileName="whoami.exe" 
    } include: [aid, ComputerName, FileName],
    // Search for net executions on Windows
    net: {
         #event_simpleName=ProcessRollup2 event_platform=Win FileName=/^net1?\.exe$/
          | aid <=> whoami.aid
          } include: [aid, ComputerName, FileName],
    // Search for systeminfo executions on Windows
    systeminfo: {
         #event_simpleName=ProcessRollup2 event_platform=Win FileName="systeminfo.exe"
          | aid <=> net.aid
          } include: [aid, ComputerName, FileName],
sequence=false, within=5m)
```

[correlate documentation](https://library.humio.com/data-analysis/functions-correlate.html)