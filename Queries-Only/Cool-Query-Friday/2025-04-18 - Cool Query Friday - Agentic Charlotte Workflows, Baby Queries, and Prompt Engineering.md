---
title: "Agentic Charlotte Workflows, Baby Queries, and Prompt Engineering"
date: 2025-04-18
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1k26eov/20250418_cool_query_friday_agentic_charlotte/"
mitre: []
series: Cool Query Friday
---

# Agentic Charlotte Workflows, Baby Queries, and Prompt Engineering

> Source: [https://www.reddit.com/r/crowdstrike/comments/1k26eov/20250418_cool_query_friday_agentic_charlotte/](https://www.reddit.com/r/crowdstrike/comments/1k26eov/20250418_cool_query_friday_agentic_charlotte/) — by Andrew-CS (CrowdStrike) — 2025-04-18

Welcome to our eighty-fifth installment of Cool Query Friday (on a Monday). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
// Get UserLogon events for Windows RDP sessions
#event_simpleName=UserLogon event_platform=Win LogonType=10 RemoteAddressIP4=*

// Omit results if the RemoteAddressIP4 field is RFC1819
| !cidr(RemoteAddressIP4, subnet=["224.0.0.0/4", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "127.0.0.1/32", "169.254.0.0/16", "0.0.0.0/32"])

// Create UserName + UserSid Hash
| UserHash:=concat([UserName, UserSid]) | UserHash:=crypto:md5([UserHash])

// Perform initial aggregation; groupBy() will sort by UserHash then LogonTime
| groupBy([UserHash, LogonTime], function=[collect([UserName, UserSid, RemoteAddressIP4, ComputerName, aid])], limit=max)

// Get geoIP for Remote IP
| ipLocation(RemoteAddressIP4)


// Use new neighbor() function to get results for previous row
| neighbor([LogonTime, RemoteAddressIP4, UserHash, RemoteAddressIP4.country, RemoteAddressIP4.lat, RemoteAddressIP4.lon, ComputerName], prefix=prev)

// Make sure neighbor() sequence does not span UserHash values; will occur at the end of a series
| test(UserHash==prev.UserHash)

// Calculate logon time delta in milliseconds from LogonTime to prev.LogonTime and round
| LogonDelta:=(LogonTime-prev.LogonTime)*1000
| LogonDelta:=round(LogonDelta)

// Turn logon time delta from milliseconds to human readable
| TimeToTravel:=formatDuration(LogonDelta, precision=2)

// Calculate distance between Login 1 and Login 2
| DistanceKm:=(geography:distance(lat1="RemoteAddressIP4.lat", lat2="prev.RemoteAddressIP4.lat", lon1="RemoteAddressIP4.lon", lon2="prev.RemoteAddressIP4.lon"))/1000 | DistanceKm:=round(DistanceKm)

// Calculate speed required to get from Login 1 to Login 2
| SpeedKph:=DistanceKm/(LogonDelta/1000/60/60) | SpeedKph:=round(SpeedKph)

// SET THRESHOLD: 1234kph is MACH 1
| test(SpeedKph>1234)

// Format LogonTime Values
| LogonTime:=LogonTime*1000           | formatTime(format="%F %T %Z", as="LogonTime", field="LogonTime")
| prev.LogonTime:=prev.LogonTime*1000 | formatTime(format="%F %T %Z", as="prev.LogonTime", field="prev.LogonTime")

// Make fields easier to read
| Travel:=format(format="%s → %s", field=[prev.RemoteAddressIP4.country, RemoteAddressIP4.country])
| IPs:=format(format="%s → %s", field=[prev.RemoteAddressIP4, RemoteAddressIP4])
| Logons:=format(format="%s → %s", field=[prev.LogonTime, LogonTime])

// Output results to table and sort by highest speed
| table([aid, ComputerName, UserName, UserSid, System, IPs, Travel, DistanceKm, Logons, TimeToTravel, SpeedKph], limit=20000, sortby=SpeedKph, order=desc)

// Express SpeedKph as a value of MACH
| Mach:=SpeedKph/1234 | Mach:=round(Mach)
| Speed:=format(format="MACH %s", field=[Mach])

// Format distance and speed fields to include comma and unit of measure
| format("%,.0f km",field=["DistanceKm"], as="DistanceKm")
| format("%,.0f km/h",field=["SpeedKph"], as="SpeedKph")

// Intelligence Graph; uncomment out one cloud
| rootURL  := "https://falcon.crowdstrike.com/"
//rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/"
//rootURL  := "https://falcon.eu-1.crowdstrike.com/"
//rootURL  := "https://falcon.us-2.crowdstrike.com/"
| format("[Link](%sinvestigate/dashboards/user-search?isLive=false&sharedTime=true&start=7d&user=%s)", field=["rootURL", "UserName"], as="User Search")

// Drop unwanted fields
| drop([Mach, rootURL])
```

## Query 2
```cql
#event_simpleName=UserLogon LogonType=10 event_platform=Win RemoteAddressIP4=*
| table([LogonTime, cid, aid, ComputerName, UserName, UserSid, RemoteAddressIP4])
| ipLocation(RemoteAddressIP4)
```

## Query 3
```cql
#event_simpleName=UserLogon LogonType=10 event_platform=Win RemoteAddressIP4=*
| !cidr(RemoteAddressIP4, subnet=["224.0.0.0/4", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "127.0.0.1/32", "169.254.0.0/16", "0.0.0.0/32"])
| ipLocation(RemoteAddressIP4)
| rename([[RemoteAddressIP4.country, Country], [RemoteAddressIP4.city, City], [RemoteAddressIP4.state, State], [RemoteAddressIP4.lat, Latitude], [RemoteAddressIP4.lon, Longitude]])
| table([LogonTime, cid, aid, ComputerName, UserName, UserSid, RemoteAddressIP4, Country, State, City, Latitude, Longitude], limit=20000)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Q&A

**Q — [Community] cobaltpsyche:** I am curious, if I use AI to review data and send an email, how can I set this up to NOT send an email of nothing of interest was found?

**A — [CS] Andrew-CS:** Yup! So you want to use Fusion to create a boolean variable, then prompt the LLM to populate the variable based on its findings. So say you create a variable named "Suspicious." You might ask the LLM to populate that variable with "true" if it has high confidence findings and "false" if it does not. You can then use an IF statement to say, "IF Suspicious is equal to true, email. Else, exit."

**Q — [Community] Critical_Quarter_245:** Do you have any examples of using agentic AI to triage alerts and reducing false positives? Maybe cross referencing with other data sources, threat intel, or data in a workflow?

**A — [CS] Andrew-CS:** If you have a Charlotte AI license, you have "Triage with Charlotte." That will automatically generate: 1. Recommendation (Escalate or not) 2. Escalation priority (number to give weighting to the escalation recommendation) 3. Verdict (true\_positive, false\_positive, inconclusive) 4. Verdict confidence (High, Medium, Low, Inconclusive) There is also a summary of why the above categories were set the way they were. [https://imgur.com/a/i3I4YmW](https://imgur.com/a/i3I4YmW) So you could take the r …
