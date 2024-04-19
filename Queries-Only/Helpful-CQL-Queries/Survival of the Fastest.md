```
// Get events of interest
#repo=detections 
| in(field="ExternalApiType", values=[Event_UserActivityAuditEvent, Event_EppDetectionSummaryEvent])

// Unify detection UUID
| detectID:=Attributes.composite_id | detectID:=CompositeId

// Based on event type, set the timestamp value for later calculations.
| case{
ExternalApiType=Event_UserActivityAuditEvent Attributes.update_status=closed | response_time:=@timestamp;
ExternalApiType=Event_UserActivityAuditEvent Attributes.assign_to_user_id=* | assign_time:=@timestamp;
ExternalApiType=Event_EppDetectionSummaryEvent | detect_time:=@timestamp;
}

// Perform aggregation against detectID to get required values
| groupBy([detectID], function=([count(ExternalApiType, distinct=true), selectLast([Hostname, Attributes.update_status]), max(Severity, as=Severity), collect([Tactic, Technique, FalconHostLink, Attributes.add_tag]), min(detect_time, as=FirstDetect), min(assign_time, as=FirstAssign), min(response_time, as=ResolvedTime)]), limit=200000)

// Check to make sure Hostname value is not null; makes sure there isn't only a detection update event.
| Hostname=*

// This handles when an alert was closed and then reopened
| case{
Attributes.update_status!=closed | ResolvedTime:="";
*;
}

// Calculate durations
| ToAssign:=(FirstAssign-FirstDetect) | ToAssign:=formatDuration(field=ToAssign, precision=3)
| AssignToClose:=(ResolvedTime-FirstAssign) | AssignToClose:=formatDuration(field=AssignToClose, precision=3)
| DetectToClose:=(ResolvedTime-FirstDetect) | DetectToClose:=formatDuration(field=DetectToClose, precision=3)

// Calculate the age of open alerts
| case{
    Attributes.update_status!="closed" | Aging:=now()-FirstDetect | Aging:=formatDuration(Aging, precision=2);
    *;
}

// Set default value for field Attributes.update_status; seeing some null values and not sure why
| default(value="new", field=[Attributes.update_status])
| default(value="-", field=[FirstAssign, ResolvedTime, ToAssign, AssignToClose, DetectToClose, Aging, Tags], replaceEmpty=true)


// Format timestamps out of epoch
| FirstDetect:=formatTime(format="%F %T", field="FirstDetect")
| FirstAssign:=formatTime(format="%F %T", field="FirstAssign")
| ResolvedTime:=formatTime(format="%F %T", field="ResolvedTime")

// Create hyperlink to detection
| format("[Detection Link](%s)", field=[FalconHostLink], as="Detection Link")

// Drop uneeded fields
| drop([detectID, _count, FalconHostLink])

// Rename field with silly name
|rename(field=[[Attributes.update_status, "CurrentState"], ["Attributes.add_tag", Tags]])

// Order output columns to make them pretty
| table([Hostname, Tactic, Technique, Severity, CurrentState, Aging, FirstDetect, FirstAssign, ResolvedTime, ToAssign, AssignToClose, DetectToClose, Tags, "Detection Link"], limit=20000)
```