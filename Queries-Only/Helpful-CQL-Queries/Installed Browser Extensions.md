Aggregate by Extension

```
#event_simpleName=InstalledBrowserExtension BrowserExtensionId!="no-extension-available"
| groupBy([event_platform, BrowserName, BrowserExtensionId, BrowserExtensionName], function=([count(aid, distinct=true, as=TotalEndpoints)]))
| format("[See Extension](https://chromewebstore.google.com/detail/%s)", field=[BrowserExtensionId], as="Chrome Store Link")
| sort(order=desc, TotalEndpoints, limit=1000)
| case{
    BrowserName="3" | BrowserName:="Chrome";
    BrowserName="4" | BrowserName:="Edge";
    *;
}
```

Aggregate by System and Browser Profile

```
#event_simpleName=InstalledBrowserExtension BrowserExtensionId!="no-extension-available"
| Extension:=format(format="%s (%s)", field=[BrowserExtensionId, BrowserExtensionName])
| groupBy([event_platform, ComputerName, UserName, BrowserProfileId, BrowserName], function=([collect([Extension])]))
| drop([_count])
| case{
    BrowserName="3" | BrowserName:="Chrome";
    BrowserName="4" | BrowserName:="Edge";
    *;
}
```