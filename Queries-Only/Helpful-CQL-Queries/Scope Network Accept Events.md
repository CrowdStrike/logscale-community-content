```
#event_simpleName=NetworkReceiveAcceptIP4 event_platform=Win
| in(field="LocalPort", values=[3389, 21, 22, 5901]) 
| !cidr(RemoteAddressIP4, subnet=["224.0.0.0/4", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "127.0.0.0/32", "169.254.0.0/16", "0.0.0.0/32"])
| communityId(proto=Protocol, sourceip=LocalAddressIP4, destinationip=RemoteAddressIP4, as=communityId)
| groupBy([communityId, RemoteAddressIP4, LocalPort], function=([count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=totalConnections)])) 
| ipLocation(RemoteAddressIP4)  
| select([RemoteAddressIP4, hostname, LocalPort, RemoteAddressIP4.country, RemoteAddressIP4.city, uniqueEndpoints, totalConnections, communityId]) 
| rdns(RemoteAddressIP4, as=rdsn) 
| asn(RemoteAddressIP4, as=asn)
| sort(uniqueEndpoints, order=desc, limit=5000)
```