---
title: "Command Line Scoring and Parsing"
date: 2021-07-30
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/ouk533/20210730_cool_query_friday_command_line_scoring/"
mitre: []
series: Cool Query Friday
---

# Command Line Scoring and Parsing

> Source: [https://www.reddit.com/r/crowdstrike/comments/ouk533/20210730_cool_query_friday_command_line_scoring/](https://www.reddit.com/r/crowdstrike/comments/ouk533/20210730_cool_query_friday_command_line_scoring/) — by Andrew-CS (CrowdStrike) — 2021-07-30

Welcome to our nineteenth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
event_platform=win event_simpleName=ProcessRollup2 (FileName=cmd.exe OR FileName=powershell.exe)
| eval cmdLength=len(CommandLine)
```

## Query 2
```cql
event_platform=win event_simpleName=ProcessRollup2 (FileName=cmd.exe OR FileName=powershell.exe)
| eval cmdLength=len(CommandLine)
| stats avg(cmdLength) as avgCmdLength max(cmdLength) as maxCmdLength min(cmdLength) as minCmdLength stdev(cmdLength) as stdevCmdLength by FileName
| eval cmdBogey=avgCmdLength+stdevCmdLength
```

## Query 3
```cql
[...]
| eval isLongCmd=if(cmdLength>160 AND FileName=="cmd.exe","2","0")
| eval isLongPS=if(cmdLength>932 AND FileName=="powershell.exe","2","0")
| eval cmdScore=isLongCmd+isLongPS
```

## Query 4
```cql
[...]
| eval carrotCount = mvcount(split(CommandLine,"^"))-1
| eval tickCount = mvcount(split(CommandLine,"`"))-1
| eval escapeCharacters=tickCount+carrotCount
| eval cmdNoEscape=trim(replace(CommandLine, "^", ""))
| eval cmdNoEscape=trim(replace(cmdNoEscape, "`", ""))
| eval cmdScore=isLongCmd+isLongPS+escapeCharacters
```

## Query 5
```cql
event_platform=win event_simpleName=ProcessRollup2 (FileName=cmd.exe OR FileName=powershell.exe)
| eval cmdLength=len(CommandLine)
| eval isLongCmd=if(cmdLength>160 AND FileName=="cmd.exe","2","0")
| eval isLongPS=if(cmdLength>932 AND FileName=="powershell.exe","2","0")
| eval carrotCount = mvcount(split(CommandLine,"^"))-1
| eval tickCount = mvcount(split(CommandLine,"`"))-1
| eval escapeCharacters=tickCount+carrotCount
| eval cmdNoEscape=trim(replace(CommandLine, "^", ""))
| eval cmdNoEscape=trim(replace(cmdNoEscape, "`", ""))
| eval cmdScore=isLongCmd+isLongPS+escapeCharacters
| fields aid ComputerName FileName CommandLine cmdLength escapeCharacters cmdScore
```

## Query 6
```cql
event_platform=win event_simpleName=ProcessRollup2 (FileName=cmd.exe OR FileName=powershell.exe)
| eval cmdLength=len(CommandLine)
| eval isLongCmd=if(cmdLength>129 AND FileName=="cmd.exe","2","0")
| eval isLongPS=if(cmdLength>1980 AND FileName=="powershell.exe","2","0")
| eval carrotCount = mvcount(split(CommandLine,"^"))-1
| eval tickCount = mvcount(split(CommandLine,"`"))-1
| eval escapeCharacters=tickCount+carrotCount
| eval cmdNoEscape=trim(replace(CommandLine, "^", ""))
| eval cmdNoEscape=trim(replace(cmdNoEscape, "`", ""))
| eval isAcceptEULA=if(like(cmdNoEscape, "%accepteula%"), "10", "0")
| eval isEncoded=if(like(cmdNoEscape, "% -e%"), "5", "0")
| eval isBypass=if(like(cmdNoEscape, "% bypass %"), "5", "0")
| eval invokePS=if(like(cmdNoEscape, "%powershell%"), "1", "0")
| eval invokeWMIC=if(like(cmdNoEscape, "%wmic%"), "3", "0")
| eval invokeCscript=if(like(cmdNoEscape, "%cscript%"), "3", "0")
| eval invokeWscipt=if(like(cmdNoEscape, "%wscript%"), "3", "0")
| eval invokeHttp=if(like(cmdNoEscape, "%http%"), "3", "0")
| eval isSystemUser=if(like(cmdNoEscape, "S-1-5-18"), "0", "1")
| eval stdOutRedirection=if(like(cmdNoEscape, "%>%"), "1", "0")
| eval isHidden=if(like(cmdNoEscape, "%hidden%"), "3", "0")
| eval cmdScore=isLongCmd+escapeCharacters+isAcceptEULA+isEncoded+isBypass+invokePS+invokeWMIC+invokeCscript+invokeWscipt+invokeHttp+isSystemUser+stdOutRedirection+isHidden
| stats dc(aid) as uniqueSystems count(aid) as exeuctionCount by FileName, cmdScore, CommandLine, cmdLength, isLongCmd, escapeCharacters, isAcceptEULA, isEncoded, isBypass, invokePS, invokeWMIC, invokeCscript, invokeWscipt, invokeHttp, isSystemUser, stdOutRedirection, isHidden
| eval CommandLine=substr(CommandLine,1,250)
| sort - cmdScore
```

## Query 7
```cql
event_platform=win event_simpleName=ProcessRollup2 (FileName=cmd.exe OR FileName=powershell.exe)
| search ParentBaseFileName!=tainium.exe
| eval cmdLength=len(CommandLine)
```

## Query 8
```cql
event_platform=win event_simpleName=ProcessRollup2 (FileName=cmd.exe OR FileName=powershell.exe)
| search CommandLine!="C:\\ProgramData\\EC2-Windows\\*"
| eval cmdLength=len(CommandLine)
```
