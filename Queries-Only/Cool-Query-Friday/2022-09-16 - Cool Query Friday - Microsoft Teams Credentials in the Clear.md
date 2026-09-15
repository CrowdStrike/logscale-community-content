---
title: "Microsoft Teams Credentials in the Clear"
date: 2022-09-16
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/xfqtyb/20220916_cool_query_friday_microsoft_teams/"
mitre: [T1552.001]
series: Cool Query Friday
---

# Microsoft Teams Credentials in the Clear

> Source: [https://www.reddit.com/r/crowdstrike/comments/xfqtyb/20220916_cool_query_friday_microsoft_teams/](https://www.reddit.com/r/crowdstrike/comments/xfqtyb/20220916_cool_query_friday_microsoft_teams/) — by Andrew-CS (CrowdStrike) — 2022-09-16

Welcome to our forty-ninth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
event_platform IN (win, mac, lin) event_simpleName=ProcessRollup2
| regex CommandLine="(?i).*(\\\\|\/)microsoft(\\\\|\/)(microsoft\s)?teams(\\\\|\/)(cookies|local\s+storage(\\\\|\/)leveldb).*"
```

## Query 2
```cql
event_platform IN (win, mac, lin) event_simpleName=ProcessRollup2
| regex CommandLine="(?i).*(\\\\|\/)microsoft(\\\\|\/)(microsoft\s)?teams(\\\\|\/)(cookies|local\s+storage(\\\\|\/)leveldb).*"
| stats dc(aid) as uniqueEndpoints, count(aid) as invocationCount, earliest(ProcessStartTime_decimal) as firstRun, latest(ProcessStartTime_decimal) as lastRun, values(CommandLine) as cmdLines by ParentBaseFileName, FileName
| convert ctime(firstRun), ctime(lastRun)
```

## Query 3
```cql
Rule Type: Process Creation
Action To Take: <choose>
Severity: <choose>
GRANDPARENT IMAGE FILENAME: .*
GRANDPARENT COMMAND LINE: .*
PARENT IMAGE FILENAME: .*
PARENT COMMAND LINE: .*
IMAGE FILENAME: .*
COMMAND LINE: .*\\Microsoft\\Teams\\(Cookies|Local\s+Storage\\leveldb).*
```

## Query 4
```cql
Rule Type: Process Creation
Action To Take: <choose>
Severity: <choose>
GRANDPARENT IMAGE FILENAME: .*
GRANDPARENT COMMAND LINE: .*
PARENT IMAGE FILENAME: .*
PARENT COMMAND LINE: .*
IMAGE FILENAME: .*
COMMAND LINE: .*\/Library\/Application\s+Support\/Microsoft\/Teams\/(Cookies|Local\s+Storage\/leveldb).*
```

## Query 5
```cql
Rule Type: Process Creation
Action To Take: <choose>
Severity: <choose>
GRANDPARENT IMAGE FILENAME: .*
GRANDPARENT COMMAND LINE: .*
PARENT IMAGE FILENAME: .*
PARENT COMMAND LINE: .*
IMAGE FILENAME: .*
COMMAND LINE: .*\/\.config\/Microsoft\/Microsoft\sTeams\/(Cookies|Local\s+Storage\/leveldb).*
```

## Query 6
```cql
#event_simpleName=ProcessRollup2
| CommandLine=/(\/|\\)Microsoft(\/|\\)(Microsoft\s)?Teams(\/|\\)(Cookies|Local\s+Storage(\/|\\)leveldb)/i
| CommandLine=/Teams(\\|\/)(local\sstorage(\\|\/))?(?<teamsFile>(leveldb|cookies))/i
| groupBy([ParentBaseFileName, ImageFileName, teamsFile, CommandLine])
```

## Query 7
```cql
#event_simpleName=ProcessRollup2
| CommandLine=/(\/|\\)Microsoft(\/|\\)(Microsoft\s)?Teams(\/|\\)(Cookies|Local\s+Storage(\/|\\)leveldb)/i
| CommandLine=/Teams(\\|\/)(local\sstorage(\\|\/))?(?<teamsFile>(leveldb|cookies))/i
| sankey(source="ImageFileName",target="teamsFile", weight=count(aid))
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
| CommandLine IN (cookies, leveldb)
```
— [CS] Andrew-CS · comment score 2

```cql
index=main event_simpleName IN ("SyntheticProcessRollup2", "ProcessRollup2") ((FilePath IN ("\\Device\\HarddiskVolume*\\Users\\*\\AppData\\*\\Microsoft\\Teams\\Cookies\\", "\\Device\\HarddiskVolume*\\Users\\*\\AppData\\*\\Microsoft\\Teams\\Local Storage\\leveldb\\") OR CommandLine IN ("*Microsoft\\Teams\\Cookies\\*", "*Microsoft\\Teams\\Local Storage\\leveldb\\*") ) FileName!="Teams.exe" event_platform=Win ) OR ((FilePath IN ("/*/Library/Application Support/Microsoft/Teams/Cookies", "/*/Library/Application Support/Microsoft/Teams/Local Storage/leveldb") OR CommandLine IN ("/*/Library/Application Support/Microsoft/Teams/Cookies/*", "/*/Library/Application Support/Microsoft/Teams/Local Storage/leveldb/*") event_platform=mac) OR ((FilePath IN ("/*/.config/Microsoft/Microsoft Teams/Cookies/", "/*/.config/Microsoft/Microsoft Teams/Local Storage/leveldb/") OR CommandLine IN ("/*/.config/Microsoft/Microsoft Teams/Cookies/*", "/*/.config/Microsoft/Microsoft Teams/Local Storage/leveldb/*") event_platform=lin)
| fillnull value="Value not provided" 
| stats values(FilePath) AS Path,
    values(CommandLine) AS commands,
    values(_time) AS Time
    BY 
    FileName,
    ComputerName,
    UserName,
    aid,
    company,
    LocalAddressIP4 
| eval Time = strftime(Time, "%m/%d/%Y %H:%M:%S")
```
— [Community] ChirsF · comment score 3

```cql
index=main sourcetype=ProcessRollup2* event_simpleName=ProcessRollup2 event_platform IN (win, mac, lin)
| regex CommandLine="(?i).*(\\\\|\/)microsoft(\\\\|\/)(microsoft\s)?teams(\\\\|\/)(cookies|local\s+storage(\\\\|\/)leveldb).*"
| stats dc(aid) as uniqueEndpoints, count(aid) as invocationCount, earliest(ProcessStartTime_decimal) as firstRun, latest(ProcessStartTime_decimal) as lastRun, values(CommandLine) as cmdLines by ParentBaseFileName, FileName
| convert ctime(firstRun), ctime(lastRun)
```
— [CS] Andrew-CS · comment score 3

### Operational caveats

> Regex is scary to look at, but easy to learn if someone explains it. We did a short write-up on it [here](https://www.reddit.com/r/crowdstrike/comments/ppzp59/20210917_cool_query_friday_regular_expressions/). The general rule is: if you want to use a character that isn't a literal number \[0-9\] or letter \[A-Z\] you should "escape" it. Here is an example. Device\HarddiskVolume1\Program Files\Adobe Suite 4\Photoshop_v1234.exe so if you wanted to write regex to match that, you just go slowly from left to right and use pattern where you can. Device\\HarddiskVolume\d\\Program\sFiles\\Adobe\sSuite\s\d\\Photoshop\_v\d{4}\.exe If I were to put actual spaces between the regex so it's easier to read …
— [CS] Andrew-CS · score 2

> Confirmed working as expected here on macOS 12.6. [https://imgur.com/a/3XcH56z](https://imgur.com/a/3XcH56z) I would make sure: 1. Custom IOA logic is correct 2. Rule is enabled 3. Custom IOA Group is enabled 4. Custom IOA Group is assigned to the prevention policy your system is in 5. Sensor has Full Disk Access If that doesn't work, you can definitely open up a support ticket for assistance.
— [CS] Andrew-CS · score 2

### Q&A

**Q — [Community] ChirsF:** From an spl perspective this is taking all events and then running the regex command on the data, versus doing CommandLine IN (“string”, “string2”) grabbing only the relevant events. Have you found this regex method to be more efficient in CS?

**A — [CS] Andrew-CS:** HI there. I like regex because of the pattern matching and precision in this instance. If you use: | CommandLine IN (cookies, leveldb) there will likely be far more *hits* that don't necessarily have to do with Teams. But please do whatever works for you!

**Q — [Community] TerribleSessions:** Is it possible to make the query bit lighter? On a large estate this never finish.

**A — [CS] Andrew-CS:** Hi there. You may have to run this in smaller time chunks on larger estates as this query will run a regex over every single command line — this is, as you've seen, computationally expensive. I've added a little optimization here by specifying index and sourcetype, but I honestly don't think that will impact the expensive part of the query. index=main sourcetype=ProcessRollup2* event_simpleName=ProcessRollup2 event_platform IN (win, mac, lin) | regex CommandLine="(?i).*(\\\\|\/)microsoft(\\\\|\/ …

**Q — [Community] Parking_Industry_761:** Is there a reason as to why we wouldn't want to exclude the teams.exe since Vectra stated that we should be looking for anything other process other than teams.exe accessing these files?

**A — [CS] Andrew-CS:** Hi there. It’s a good question. What we’re hunting here are things invoking the files via command line which we would not expect Teams to do when reading them. I hope that helps.
