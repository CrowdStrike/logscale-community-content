The `rdns` function resolves hostnames using reverse DNS lookups.

If a lookup fails, it will keep the event but not add the given field.

The number of resulting events from this function is limited by the configuration parameter [`MAX_STATE_LIMIT`](https://library.humio.com/falcon-logscale-self-hosted/envar-max-state-limit.html), whose default limit is 20000. If the number of events exceeds this limit, the result will be truncated with a warning.

To prevent the `rdns` function from blocking query execution for an indeterminate amount of time, a timeout is applied to all RDNS requests. If an RDNS request doesn't return a result within the timeout, the lookup is considered to have failed for the associated event. However, if the request eventually returns, its result is added to an internal cache within LogScale for a period of time. Therefore, a static query using the `rdns` function may fail a lookup for an event on its first execution, but succeed in a subsequent execution. In live queries this behaviour is less of a problem, as the `rdns` function will be evaluated continually. Thus, it is preferable to mainly use the `rdns` function in live queries.

```
| rdns(RemoteAddressIP4, as=rdns)
| select([RemoteAddressIP4, rdns])
```

[rdns Documentation](https://library.humio.com/data-analysis/functions-rdns.html)
