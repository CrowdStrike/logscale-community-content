```
// Get events of interest
#repo=detections 
| in(field="ExternalApiType", values=[Event_UserActivityAuditEvent, Event_EppDetectionSummaryEvent])

// Unify detection UUID
| detectID:=Attributes.detection_id | detectID:=DetectId

// Based on event type, set the timestamp value for later calculations.
| case{
ExternalApiType=Event_UserActivityAuditEvent Attributes.update_status=closed | response_time:=@timestamp;
ExternalApiType=Event_UserActivityAuditEvent Attributes.assign_to_uuid=* | assign_time:=@timestamp;
ExternalApiType=Event_EppDetectionSummaryEvent | detect_time:=@timestamp;
}

// Perform aggregation against detectID to get required values
| groupBy([detectID], function=([count(ExternalApiType, distinct=true), selectLast([ComputerName, Attributes.update_status]), max(Severity, as=Severity), collect([Tactic, Technique, FalconHostLink]), min(detect_time, as=FirstDetect), min(assign_time, as=FirstAssign), min(response_time, as=ResolvedTime)]), limit=200000)

// Check to make sure ComputerName value is not null; makes sure there isn't only a detection update event.
| ComputerName=*

// This handles when an alert was closed and then reopened
| case{
Attributes.update_status!=closed | ResolvedTime:="";
*;
}

// Calculate minutes to assign
| MinutesToAssign:=(FirstAssign-FirstDetect)/1000/60 | round("MinutesToAssign")

// Calculate hours from assign to close
| HoursFromAssignToClose:=(ResolvedTime-FirstAssign)/1000/60/60 | round("HoursFromAssignToClose")

// Calculate days from detect to close
| DaysFromDetectToClose:=(ResolvedTime-FirstDetect)/1000/60/60/24 | round("DaysFromDetectToClose")

// Set default values for fields FirstAssign, ResolvedTime, MinutesToAssign, HoursFromAssignToClose, DaysFromDetectToClose
| default(value="-", field=[FirstAssign, ResolvedTime, MinutesToAssign, HoursFromAssignToClose, DaysFromDetectToClose], replaceEmpty=true)

// Set default value for field Attributes.update_status; seeing some null values and not sure why
| default(value="new", field=[Attributes.update_status])

// Format timestamps out of epoch
| FirstDetect:=formatTime(format="%F %T", field="FirstDetect")
| FirstAssign:=formatTime(format="%F %T", field="FirstAssign")
| ResolvedTime:=formatTime(format="%F %T", field="ResolvedTime")

// Create hyperlink to detection
| format("[Detection Link](%s)", field=[FalconHostLink], as="Detection Link")

// Drop uneeded fields
| drop([detectID, _count, FalconHostLink])

// Rename field with silly name
|rename(field=[[Attributes.update_status, "CurrentState"]])

// Order output columns to make them pretty
| table([ComputerName, Tactic, Technique, Severity, CurrentState, FirstDetect, FirstAssign, ResolvedTime, MinutesToAssign, HoursFromAssignToClose, DaysFromDetectToClose, "Detection Link"], limit=20000)
```