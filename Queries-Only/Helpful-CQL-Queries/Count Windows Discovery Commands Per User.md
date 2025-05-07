```
// Insert Discovery commands of interest here
event_platform=Win #event_simpleName=ProcessRollup2 FileName=/(whoami|ping|net1?|systeminfo|quser|ipconfig)/iF

// Restrict to non-system UserSid Values
| UserSid=S-1-5-21-*

// User case() to create discovery command counter
| case {
    FileName=/whoami/iF     | whoami:="1";
    FileName=/ping/iF       | ping:="1";
    FileName=/net1?/iF      | net:="1";
    FileName=/systeminfo/iF | systeminfo:="1";
    FileName=/quser/iF      | quser:="1";
    FileName=/ipconfig/iF   | ipconfig:="1";
}

// Aggregate results by duration used in time picker
| groupBy([UserName, UserSid], function=([sum(whoami, as=whoami), sum(ping, as=ping), sum(net, as=net), sum(systeminfo, as=systeminfo), sum(quser, as=quser), sum(ipconfig, as=ipconfig), selectLast([CommandLine])]), limit=max)

// Rename field for clarity
| rename(field="CommandLine", as="LastCommandRun")

// Get total number of discovery commands run per UserName/UserSid key pair
| totalDiscovery:=whoami+ping+net+systeminfo+quser+ipconfig

// Set threshold for commands runs (optional)
| totalDiscovery>5

// Reorder using table for easier reading
| table([UserName, UserSid, totalDiscovery, whoami, ping, net, systeminfo, quser, ipconfig, LastCommandRun])
```