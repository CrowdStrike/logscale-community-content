```
#event_simpleName=CriticalEnvironmentVariableChanged
| EnvironmentVariableName =/(SSH_CONNECTION|USER)/
| EnvironmentVariableValue=/(?<userName>\S+)\n(?<localIP>\d+\.\d+\.\d+\.\d+)\s+(?<localPort>\d+)\s+(?<remoteIP>\d+\.\d+\.\d+\.\d+)\s+(?<remotePort>\d+)$/i
| table([@timestamp, aid, userName, remoteIP, remotePort, localIP, localPort])
| "Process Explorer" := format("[Process Explorer](https://falcon.crowdstrike.com/investigate/process-explorer/%s/%s)", field=["aid", "ContextProcessId"])
```

[[regex]] | [[regex - extraction]] | [[table]] | [[format - hyperlinks]]
