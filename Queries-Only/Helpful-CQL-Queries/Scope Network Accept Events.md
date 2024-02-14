```
#event_simpleName=NetworkReceiveAcceptIP4 event_platform=Win

| in(field="LocalPort", values=[3389, 21, 22, 5901])
| !cidr(RemoteAddressIP4, subnet=["224.0.0.0/4", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "127.0.0.0/32", "169.254.0.0/16", "0.0.0.0/32"])

|communityId(
     proto=Protocol,
     sourceip=LocalAddressIP4,
     destinationip=RemoteAddressIP4,
     as=communityId)

| $Protocol()
| groupBy([communityId, RemoteAddressIP4, LocalPort], function=([count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=totalConnections)]))
| ipLocation(RemoteAddressIP4)
| match(file="service-names-port-numbers.csv", column=LocalPort, field=LocalPort, include=ServiceName, ignoreCase=true, strict=false)
| rdns("RemoteAddressIP4")
| select([RemoteAddressIP4, hostname, LocalPort, Protocol, ServiceName, RemoteAddressIP4.country, RemoteAddressIP4.city, uniqueEndpoints, totalConnections])
| sort(uniqueEndpoints, order=desc, limit=5000)

```