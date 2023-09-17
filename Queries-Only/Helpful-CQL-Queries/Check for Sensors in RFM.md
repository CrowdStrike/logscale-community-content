```
#event_simpleName=OsVersionInfo
| osData:=concat([OSVersionString, ProductName])
| groupBy([aid], function=([selectFromMax(field="@timestamp", include=[event_platform, RFMState, LinuxSensorBackend, AgentVersion, osData])]))
| RFMState match {
    1 => RFMState := "RFM" ;
    0 => RFMState := "OK" ;
}
| case {
    event_platform!=Lin | LinuxSensorBackend:="NA";
    *;
}
| LinuxSensorBackend match {
    1 => LinuxSensorBackend := "eBPF" ;
    0 => LinuxSensorBackend := "Kernel" ;
    "NA" => LinuxSensorBackend := "-" ;
}
```
