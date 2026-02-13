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

Enhanced version:
```
// Get browser extension event
#event_simpleName=InstalledBrowserExtension BrowserExtensionId!="no-extension-available"
| aid=?aid
| ComputerName=?ComputerName

// Normalize timestamps
| BrowserExtensionInstalledTimestamp:=BrowserExtensionInstalledTimestamp*1000
| formatTime(format="%Y-%m-%dT%H:%M:%S.%L", field="BrowserExtensionInstalledTimestamp", as="ExtensionInstalledDateTime")
// Convert browser name from decimal to human readable
| case{
  BrowserName="1" | BrowserName:="Firefox";
  BrowserName="2" | BrowserName:="Safari" | format("[See Extension](https://apps.apple.com/us/app/%s)", field=[BrowserExtensionId], as="ExtensionLink");
  BrowserName="3" | BrowserName:="Chrome" | format("[See Extension](https://chromewebstore.google.com/detail/%s)", field=[BrowserExtensionId], as="ExtensionLink");
  BrowserName="4" | BrowserName:="Edge" | format("[See Extension](https://microsoftedge.microsoft.com/addons/detail/%s)", field=[BrowserExtensionId], as="ExtensionLink");
  *;
}
// Special case for Firefox
| case {
  BrowserName="Firefox" | BrowserExtensionPath=/@((dictionaries|services)\.addons|firefox\.)?mozilla\.(org|com)\.xpi$/i | format("[No extension link](https://addons.mozilla.org/en-US/firefox/extensions)", field=[], as="ExtensionLink");
  BrowserName="Firefox" | BrowserExtensionPath!=/@((dictionaries|services)\.addons|firefox\.)?mozilla\.(org|com)\.xpi$/i | format("[See Extension](https://addons.mozilla.org/en-US/firefox/addon/%s)", field=[BrowserExtensionId], as="ExtensionLink");
  *;
}
| BrowserName=?BrowserName
| BrowserExtensionName=?BrowserExtensionName
| BrowserExtensionId=?BrowserExtensionId
// Convert install method from decimal to human readable
| case{
  BrowserExtensionInstallMethod="1" | BrowserExtensionInstallMethod:="Browser Default";
  BrowserExtensionInstallMethod="2" | BrowserExtensionInstallMethod:="Web Store";
  BrowserExtensionInstallMethod="3" | BrowserExtensionInstallMethod:="Enterprise Managed";
  BrowserExtensionInstallMethod="4" | BrowserExtensionInstallMethod:="Unidentified";
  BrowserExtensionInstallMethod="5" | BrowserExtensionInstallMethod:="Web Store third-party";
  BrowserExtensionInstallMethod="6" | BrowserExtensionInstallMethod:="Developer Mode";
  *;
}
| case {
  BrowserExtensionStatusEnabled=1 | BrowserExtensionStatusEnabled:="Yes";
  BrowserExtensionStatusEnabled=* | BrowserExtensionStatusEnabled:="No";
}
| groupBy([aid, ComputerName, BrowserName, BrowserExtensionId, BrowserExtensionName, BrowserExtensionVersion, ExtensionLink], function=[collect([BrowserProfileId, BrowserExtensionInstallMethod, BrowserExtensionStatusEnabled, ExtensionInstalledDateTime])], limit=max)
| sort(timestamp, order=desc, limit=max)
```
