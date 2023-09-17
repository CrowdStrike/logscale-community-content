```
rootURL  := "https://falcon.crowdstrike.com/" ;
//rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/" ;
//rootURL  := "https://falcon.eu-1.crowdstrike.com/" ;
//rootURL  := "https://falcon.us-2.crowdstrike.com/" ;
 

// Make writing the URL a bit easier. 
| colon := "%3A"
| tick  := "%27"
| plus  := "%2B"

// Virus Total
| format("[Virus Total](https://www.virustotal.com/gui/file/%s)", field=[SHA256HashData], as="VT")

// Hybrid Analysis
| format("[Hybrid Analysis](https://www.hybrid-analysis.com/search?query=%s)", field=[SHA256HashData], as="HA")

// Intelligence Graph
| format("[Indicator Graph](%sintelligence/graph?indicators=hash%s%s%s%s)", field=["rootURL", "colon", "tick", "SHA256HashData", "tick"], as="Indicator Graph")
```

```
// Graph Explorer
| rootURL  := "https://falcon.crowdstrike.com/" /* US-1 */
//| rootURL  := "https://falcon.us-2.crowdstrike.com/" /* US-2 */
//| rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/" /* Gov */
//| rootURL  := "https://falcon.eu-1.crowdstrike.com/"  /* EU */
| format("[Graph Explorer](%sgraphs/process-explorer/graph?id=pid:%s:%s)", field=["rootURL", "aid", "falconPID"], as="Graph Explorer") 
```

[format Documentation](https://library.humio.com/data-analysis/functions-format.html#functions-format-examples)

