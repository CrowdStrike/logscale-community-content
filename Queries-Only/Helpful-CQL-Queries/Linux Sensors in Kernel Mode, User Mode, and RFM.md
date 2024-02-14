NEW WAY

```
#event_simpleName=OsVersionInfo event_platform=Lin

| LinuxSensorBackend=*
| case{

    LinuxSensorBackend=0 | LinuxSensorBackend := "Kernel";
    LinuxSensorBackend=1 | LinuxSensorBackend := "eBPF";
    *;
}

| groupBy([aid], function=(selectLast([AgentVersion, LinuxSensorBackend, OSVersionFileData])))
| replace("([0-9A-Fa-f]{2})", with="%$1", field=OSVersionFileData, as=OSVersionFileData)
| OSVersionFileData:=urlDecode("OSVersionFileData")
| regex("PRETTY_NAME=\"(?<DistroName>[^\"]+)\"", field=OSVersionFileData, strict=false)
| select([aid, AgentVersion, LinuxSensorBackend, DistroName, OSVersionFileData])

```

OLD WAY

```
#event_simpleName=/(OsVersionInfo|ConfigStateUpdate|SensorHeartbeat)/

| event_platform=Lin
| groupBy([cid, aid], function=([selectLast([ConfigStateData, OSVersionString, SensorStateBitMap])]))
| ConfigStateData match {

    /1400000000c4/ => isInUserMode:="1" ;
    *              => isInUserMode:="0" ;
  }

| SensorStateBitMap match {

    2 => isInRFM:="1" ;
    0 => isInRFM:="0" ;
  }

| case {

		 isInUserMode=1 AND isInRFM=1 | message := "User Mode Enabled" ;

     	 isInUserMode=0 AND isInRFM=0 | message := "Kernel Mode Enabled" ;
     	 isInUserMode=0 AND isInRFM=1 | message := "RFM" ;
  * }

| OSVersionString = /^Linux\s(?<hostName>\S+)\s(?<kernelVersion>\S+)\s/i
| aid=?aid hostName=?hostName message=?message
| select([aid, hostName, Version, kernelVersion, isInRFM, isInUserMode, message])

```