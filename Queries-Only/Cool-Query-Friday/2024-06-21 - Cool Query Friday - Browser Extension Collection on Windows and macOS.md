---
title: "Browser Extension Collection on Windows and macOS"
date: 2024-06-21
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1dl3bo5/20240621_cool_query_friday_browser_extension/"
mitre: []
series: Cool Query Friday
---

# Browser Extension Collection on Windows and macOS

> Source: [https://www.reddit.com/r/crowdstrike/comments/1dl3bo5/20240621_cool_query_friday_browser_extension/](https://www.reddit.com/r/crowdstrike/comments/1dl3bo5/20240621_cool_query_friday_browser_extension/) — by Andrew-CS (CrowdStrike) — 2024-06-21

Welcome to our seventy-sixth installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
#event_simpleName=InstalledBrowserExtension
| fieldstats()
```

## Query 2
```cql
#event_simpleName=InstalledBrowserExtension BrowserExtensionId!="no-extension-available"
| groupBy([event_platform, BrowserName, BrowserExtensionId, BrowserExtensionName], function=([count(aid, distinct=true, as=TotalEndpoints)]))
```

## Query 3
```cql
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

## Query 4
```cql
// Get browser extension event
#event_simpleName=InstalledBrowserExtension BrowserExtensionId!="no-extension-available"
// Aggregate by BrowserName
| groupBy([BrowserExtensionName], function=([count(aid, distinct=true, as=TotalEndpoints)]))
| sort(TotalEndpoints, order=desc)
```

## Query 5
```cql
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

## Query 6
```cql
// Get browser extension event
#event_simpleName=InstalledBrowserExtension BrowserExtensionId!="no-extension-available"
// Look for side loaded extensions or extensions from third-party stores
| in(field="BrowserExtensionInstallMethod", values=[4,5])
// Make a new field that includes the extension ID and Name
| Extension:=format(format="%s (%s)", field=[BrowserExtensionId, BrowserExtensionName])
// Aggregate by endpoint and browser profile
| groupBy([event_platform, aid, ComputerName, UserName, BrowserProfileId, BrowserName, BrowserExtensionInstallMethod], function=([collect([Extension])]))
// Get unnecessary field
| drop([_count])
// Convert browser name from decimal to human readable
| case{
BrowserName="3" | BrowserName:="Chrome";
BrowserName="4" | BrowserName:="Edge";
*;
}
// Convert install method from decimal to human readable
| case{
BrowserExtensionInstallMethod="4" | BrowserExtensionInstallMethod:="Sideload";
BrowserExtensionInstallMethod="5" | BrowserExtensionInstallMethod:="Third-Party Store";
*;
}
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
| !in(BrowserExtensionId, values=[
aapocclcgogkmnckokdopfmhonfmgoek, // (Slides)
aohghmighlieiainnegkcijnfilokake, // (Docs)
lmjegmlicamnimmfhcmpkclmigmmcbeh, // (Application Launcher For Drive (by Google))
ghbmnnjooekpmoecnnnilnnbdlolhkhi, // (Google Docs Offline)
felcaaldnbdncclmgdcncolpebgiejap, // (Sheets)
jlhmfgmfgeifomenelglieieghnjghma, // (Cisco Webex Extension)
jhknlonaankphkkbnmjdlpehkinifeeg, // (Google Forms)
nmmhkkegccagdldgiimedpiccmgmieda, // (Chrome Web Store Payments)
nckgahadagoaajjgafhacjanaoiihapd // (Google Hangouts)
])
```
— [Community] blahdidbert · comment score 2

```cql
| !match(file="good_extensions.csv", column="BrowserExtensionId", field=BrowserExtensionId)
```
— [CS] Andrew-CS · comment score 1

```cql
// Get browser extension event
#event_simpleName=InstalledBrowserExtension BrowserExtensionId!="no-extension-available"
// Normalize timestamp
| BrowserExtensionInstalledTimestamp:=BrowserExtensionInstalledTimestamp*1000
// Get detla from install time to now in milliseconds
| InstallDelta:=now()-BrowserExtensionInstalledTimestamp
// Check to see if installed in last 7 days in milliseconds
| InstallDelta>=86400000
```
— [CS] Andrew-CS · comment score 1

### Q&A

**Q — [Community] blahdidbert:** Absolutely true but a couple questions: 1. What are the roles that someone needs to have to create, update, delete lookup files? 2. What would be the syntax to exclude a lookup file instead?

**A — [CS] Andrew-CS:** 1. Falcon Admin &#8203; | !match(file="good_extensions.csv", column="BrowserExtensionId", field=BrowserExtensionId) You would want to upload a csv with the column BrowserExtensionId that includes the common or allowed extensions. This would exclude them from results. You could also manage a list of unapproved extensions and hunt against that list.

**Q — [Community] festivusmiracle:** So how do you know what the numerical values for some of these fields represents? Like for the BrowserName=3, you convert the 3 to Chrome. And the BrowserExtensionInstallMethod=4 you convert to Sideload. Is there a way to know all of the possible values so we can make them all human readable? Thank …

**A — [CS] Andrew-CS:** Yes sir. They are in the Event Data Dictionary. There's a screen shot (second one) in the post above.

**Q — [Community] Beeefin:** Is there a way to query only recently installed browser extensions?

**A — [CS] Andrew-CS:** Yes. You can verify against the field `BrowserExtensionInstalledTimestamp`. This would be q short example. // Get browser extension event #event_simpleName=InstalledBrowserExtension BrowserExtensionId!="no-extension-available" // Normalize timestamp | BrowserExtensionInstalledTimestamp:=BrowserExtensionInstalledTimestamp*1000 // Get detla from install time to now in milliseconds | InstallDelta:=now()-BrowserExtensionInstalledTimestamp // Check to see if installed in last 7 days in milliseconds | …

**Q — [Community] Old_Organization9205:** Is it possible to group all Domain Names (URLs) which were called by each extension? Final outcome would be to lookup those URLs in a search for malicious ones.

**A — [CS] Andrew-CS:** It would not be possible to tell since the chrome process is resolving those domains and not the extension itself.
