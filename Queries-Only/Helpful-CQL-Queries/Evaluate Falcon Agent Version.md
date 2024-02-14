```
#event_simpleName=OsVersionInfo event_platform=Win

| groupby(aid, function=selectLast([AgentVersion, event_platform, @timestamp]))
| AgentVersion=/(?<majorVersion>\d+)\.(?<minorVersion>\d+)\.(?<buildNumber>\d+)\.\d+/
| case{

majorVersion = 6 AND minorVersion = 42 | buildPolicy := "Dev Build";
majorVersion = 6 AND minorVersion = 42 | buildPolicy := "N";
majorVersion = 6 AND minorVersion = 40 | buildPolicy := "N-1";
majorVersion = 6 AND minorVersion = 39 | buildPolicy := "N-2";
majorVersion = 6 AND minorVersion < 39 | buildPolicy := "N-3+";
majorVersion = 0 | buildPolicy := "Sensor Uninitialized";
}
```