The `asn` function takes a field that contains an IP address and adds Autonomous System Number (ASN) data to the query results. The added data includes the ASN identifier and ASN organization.

```
| asn(RemoteAddressIP4)
| select([RemoteAddressIP4, RemoteAddressIP4.asn, RemoteAddressIP4.org])
```

[asn Documentation](https://library.humio.com/data-analysis/functions-asn.html)