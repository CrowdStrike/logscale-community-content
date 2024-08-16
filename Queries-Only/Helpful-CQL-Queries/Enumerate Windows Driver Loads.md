```
// Get all DriverLoad events and Event_ModuleSummaryInfoEvent events so certificate data can be merged in
(#event_simpleName=DriverLoad event_platform=Win) OR (#repo=detections ExternalApiType=Event_ModuleSummaryInfoEvent )

// Shorten file path from DriverLoad event
| case{
    #event_simpleName=DriverLoad | FilePath=/Device\\HarddiskVolume\d+(?<ShortFileParth>.+$)/;
    *;
}

// Create selfJoinFilter
| selfJoinFilter(field=[SHA256HashData], where=[{#event_simpleName=DriverLoad}, {#repo=detections ExternalApiType=Event_ModuleSummaryInfoEvent}])

// Aggregate
| groupBy([SHA256HashData], function=([collect([ShortFileParth, FileName, OriginalFilename, SubjectCN, IssuerCN])]), limit=max)
| FileName=*

// Set default values
| default(value="-", field=[SubjectCN, IssuerCN, OriginalFilename])
```