```
// Get ProcessRollup2 events for Windows with Mark of the Web field set
#event_simpleName=ProcessRollup2 event_platform=Win ZoneIdentifier=*
// Parse ConfigBuild for Falcon link syntehsis

| ConfigBuild=/(?<config>\d+)\.(?<opSystem>\d+)\.(?<falconBuild>\d+)\.(?<cloudDecimal>\d+$)/i
| cloudDecimal match {

    1 => rootURL  := "https://falcon.crowdstrike.com/" ;
    9 => rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/" ;
    10 => rootURL := "https://falcon.eu-1.crowdstrike.com/" ;
    11 => rootURL := "https://falcon.us-2.crowdstrike.com/" ;
}
// Extract file name and path

| ImageFileName=/\\Device\\HarddiskVolume\d+(?<filePath>\S+\\)(?<fileName>\w+\.exe)$/i

// Group output

| groupBy([fileName, SHA256HashData, MD5HashData, rootURL], function=([collect([#event_simpleName, filePath]), count(aid, distinct=true, as=endpointCount), count(aid, as=executionCount)]))

// Virus Total Link

| format("[Virus Total](https://www.virustotal.com/gui/file/%s)", field=[SHA256HashData], as="VT")

// Hybrid Analysis Link

| format("[Hybrid Analysis](https://www.hybrid-analysis.com/search?query=%s)", field=[SHA256HashData], as="HA")

// Indicator Graph Link

| colon := "%3A"
| tick := "%27"
| plus := "%2B"
| format("[Indicator Graph](%sintelligence/graph?indicators=hash%s%s%s%s)",field=["rootURL","colon", "tick","SHA256HashData", "tick"], as="Graph")

// Order column output as desired

| select([fileName, filePath, endpointCount, executionCount, Graph, HA, VT, SHA256HashData, MD5HashData])

```