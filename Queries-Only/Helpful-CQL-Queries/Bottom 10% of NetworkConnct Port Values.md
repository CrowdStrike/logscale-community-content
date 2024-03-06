```
#event_simpleName=NetworkConnectIP4
| groupBy([RemotePort], function=count(as=count), limit=max) 
| [sum(count, as=total), sort(field=RemotePort, order=ascending, limit=20000)] 
| percent := 100 * (count / total) 
| drop([total]) 
| percent < 10
```