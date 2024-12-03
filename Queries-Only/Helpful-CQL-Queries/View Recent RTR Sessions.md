```
// Get RTR Start events
#repo=detections #event_simpleName=Event_RemoteResponseSessionStartEvent

// Rename Agent ID value
| rename(field="AgentIdString", as="aid")

// Display results in table
| table([StartTimestamp, UserName, aid], limit=20000)

// Bring in data from AID Master lookup file
| aid=~match(file="aid_master_main.csv", column=[aid], strict=false)

// Convert timestamp to human-readable value
| formatTime(format="%F %T %Z", as=StartTimestamp, field=StartTimestamp)
```