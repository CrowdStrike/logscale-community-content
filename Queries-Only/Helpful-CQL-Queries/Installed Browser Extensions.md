Aggregate by Extension

```
// Get browser extension event
#event_simpleName=InstalledBrowserExtension BrowserExtensionId!="no-extension-available"

// Aggregate by event_platform, BrowserName, ExtensionID and ExtensionName
| groupBy([event_platform, BrowserName, BrowserExtensionId, BrowserExtensionName], function=([count(aid, distinct=true, as=TotalEndpoints)]))

// Check to see if the extension is installed on fewer than 50 systems
| test(TotalEndpoints<50)

// Create a link to the Chrome Extension Store
| format("[See Extension](https://chromewebstore.google.com/detail/%s)", field=[BrowserExtensionId], as="Chrome Store Link")

// Sort in descending order
| sort(order=desc, TotalEndpoints, limit=1000)

// Convert the browser name from decimal to human-readable
| case{
    BrowserName="3" | BrowserName:="Chrome";
    BrowserName="4" | BrowserName:="Edge";
    *;
}
```

Aggregate by System and Browser Profile

```
// Get browser extension event
#event_simpleName=InstalledBrowserExtension BrowserExtensionId!="no-extension-available"

// Make a new field that includes the extension ID and Name
| Extension:=format(format="%s (%s)", field=[BrowserExtensionId, BrowserExtensionName])

// Aggregate by endpoint and browser profile
| groupBy([event_platform, aid, ComputerName, UserName, BrowserProfileId, BrowserName], function=([collect([Extension])]))

// Get unnecessary field
| drop([_count])

// Convert browser name from decimal to human readable
| case{
    BrowserName="3" | BrowserName:="Chrome";
    BrowserName="4" | BrowserName:="Edge";
    *;
}
```

Hunt for specific keyword in extension name:

```
// Get browser extension event
#event_simpleName=InstalledBrowserExtension BrowserExtensionId!="no-extension-available"

// Look for string "vpn" in extension name
| BrowserExtensionName=/vpn/i

// Make a new field that includes the extension ID and Name
| Extension:=format(format="%s (%s)", field=[BrowserExtensionId, BrowserExtensionName])

// Aggregate by endpoint and browser profile
| groupBy([event_platform, aid, ComputerName, UserName, BrowserProfileId, BrowserName], function=([collect([Extension])]))

// Get unnecessary field
| drop([_count])

// Convert browser name from decimal to human readable
| case{
    BrowserName="3" | BrowserName:="Chrome";
    BrowserName="4" | BrowserName:="Edge";
    *;
}
```