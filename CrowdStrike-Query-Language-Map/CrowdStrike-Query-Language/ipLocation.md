The `ipLocation` function determines the country, city, longitude, and latitude for an IP address (ipv4 or ipv6). The attributes `ip.country`, `ip.city, ip.lon`, `ip.lat` are added to the event.

```
| ipLocation(RemoteAddressIP4)
```

Example of using ipLocation with pre-filtering for RFC-1819 addresses:

```
| !cidr(RemoteAddressIP4, subnet=["224.0.0.0/4", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "127.0.0.1/32", "169.254.0.0/16", "0.0.0.0/32"])
| ipLocation(RemoteAddressIP4)
```

[ipLocation Documentation](https://library.humio.com/data-analysis/functions-iplocation.html)
