```
// Get UI Audit Events
#repo="detections" ExternalApiType=/Remote/

// Check commands for "get"
| array:regex("Commands[]",regex="get")

// Create unified "Commands" field
| concatArray("Commands", separator="; ", as=Commands)

// Check to make sure Commands is populated
| Commands=*

// Aggregate results
| groupBy([UserName, AgentIdString], function=([collect([Commands])]))
| groupBy([UserName], function=([count(AgentIdString, as=SystemsAccssed), collect([Commands])]))
```