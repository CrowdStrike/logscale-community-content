---
title: "SITUATIONAL AWARENESS \\\\ Hunting for NVIDIA Certificates"
date: 2022-03-06
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/t81heu/20220306_cool_query_friday_situational_awareness/"
mitre: []
series: Cool Query Friday
---

# SITUATIONAL AWARENESS \\ Hunting for NVIDIA Certificates

> Source: [https://www.reddit.com/r/crowdstrike/comments/t81heu/20220306_cool_query_friday_situational_awareness/](https://www.reddit.com/r/crowdstrike/comments/t81heu/20220306_cool_query_friday_situational_awareness/) — by Andrew-CS (CrowdStrike) — 2022-03-06

Welcome to our thirty-ninth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
index=json ExternalApiType=Event_ModuleSummaryInfoEvent 
| search SubjectCN IN ("NVIDIA Corporation") 
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName, ProductName, ProductVersion , FileDescription , FileVersion , CompanyName 
| fillnull value="Unknown" FileName, ProductName, ProductVersion , FileDescription , FileVersion , CompanyName
| stats values(SubjectDN) as SubjectDN, values(SHA256HashData) as sha256 by IssuerCN, FileName, ProductName, ProductVersion , FileDescription , FileVersion , CompanyName
| sort + FileName
```

## Query 2
```cql
index=json ExternalApiType=Event_ModuleSummaryInfoEvent 
| search SubjectSerialNumber IN (43bb437d609866286dd839e1d00309f5, 14781bc862e8dc503a559346f5dcc518) 
| lookup local=true appinfo.csv SHA256HashData OUTPUT FileName, ProductName, ProductVersion , FileDescription , FileVersion , CompanyName 
| fillnull value="Unknown" FileName, ProductName, ProductVersion , FileDescription , FileVersion , CompanyName
| stats values(SHA256HashData) as sha256 by IssuerCN, SubjectCN, SubjectDN, FileName, ProductName, ProductVersion , FileDescription , FileVersion , CompanyName
```

## Query 3
```cql
index=main sourcetype IN (ProcessRollup*, ImageHash*, PeFileWritten*, DriverLoad*) event_platform=win event_simpleName IN (ProcessRollup2, ImageHash, PeFileWritten, DriverLoad)
| search SHA256HashData IN (
17d22cf02b4121efd4526f30b16371a084f5f41b8746f9359bad4c29d7deb715
31f87d4188f210be2df99b0a88fb437628a9864a3bffea4c5238cbc7dcb14df8
31fef1519f5dd7b74d21a19b453ace2c677922b8060fea11d6f53bf8f73bd99c
4d4e71840e5802b9ab790bae15bcadb0a31b3285009189be50573e313db07fe2
6b02469349125bf474ae29303d81e84ad2f073ee6b6c619015bf7b9fea371ce6
6bf1d0b94f4097f65fd611ea570b10aff7c5141d76736b0cb001a5de60fb778b
9fac39999d2d87e0b60eedb4126fa5a25d142c52d5e5ddcd8bdb6bf2a836abb9
a86a788e4823caa25f6eb3f6c5d7e59de225f121af6ed24077e118ba324e4e19
b4226ed448e07357f216c193ca8f4ec74268e41fa369196b6de54cf058f622d1
b4bd732e766e7de094378d2dec07264e16eb6b75e9c3fa35c2219dfe3726cc27
b7c21ee31c8dea07cc5ccc9736e4aac31428f073ae14ad430dc8bdf999ab0813
cbf74c0c0f5f05a501c53ab8f96c716522096cf60f545ecadd3100b578b62900
d4210f400bcf3bc2553fc7c62493e96554c1b3b82d346db8adc84c75cea124d6
db22f4465ed5bb82e8b9322291cafc554ded1dc8ecd7d7f2b1b14784617a0f5a
ed5728d26a7856886faec9e3340ce7dbafbf8daa4c36aad79a8e7106b998d76a
f39ce105207842154e69cedd3e332b2bfefad82cdd40832245cc991dad5b8f7c
fce84e34a971e1bf8420639689c8ecc6170357354deb775c02f6d70a28723680
ff3935ba15be2d74a810b695bdc6529103ddd81df302425db2f2cafcbaf10040
)
| eval falconPID=coalesce(ContextProcessId_decimal, TargetProcessId_decimal)
| eval ProcExplorer=case(falconPID!="","https://falcon.crowdstrike.com/investigate/process-explorer/" .aid. "/" . falconPID)
| stats values(FileName) as fileName, dc(aid) as endpointCount, count(aid) as runCount, values(FilePath) as filePaths, values(event_simpleName) as eventType by SHA256HashData, ProcExplorer
```

## Query 4
```cql
index=main sourcetype IN (ProcessRollup*, ImageHash*, PeFileWritten*, DriverLoad*) event_platform=win event_simpleName IN (ProcessRollup2, ImageHash, PeFileWritten, DriverLoad)
| search SHA256HashData IN (
INSERT SHA256 LIST HERE
)
| eval falconPID=coalesce(ContextProcessId_decimal, TargetProcessId_decimal)
| eval ProcExplorer=case(falconPID!="","https://falcon.crowdstrike.com/investigate/process-explorer/" .aid. "/" . falconPID)
| rex field=FilePath ".*\\HarddiskVolume\d+(?<trimmedPath>.*)"
| stats values(FileName) as fileName, dc(aid) as endpointCount, count(aid) as runCount, values(trimmedPath) as filePaths, values(event_simpleName) as eventType by SHA256HashData
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
| inputlookup lookuptable
```
— [CS] Andrew-CS · comment score 2

### Q&A

**Q — [Community] cs-del:** Quick question, why did you search through JSON logs rather the main index. If you can give a little insight between both indexing on?

**A — [CS] Andrew-CS:** Hi there. You don't have to specify, but it will make things quicker. The JSON index is basically what will be output by the SIEM connector or ingested by our SIEM integrations. It includes alerts, audit events, etc.

**Q — [Community] MSP-IT-Simplified:** Quick question. In you first query you reference file appinfo.csv, where is that file located?

**A — [CS] Andrew-CS:** Hi there. It's a lookup table similar to `aid_master`. I have a list of the ones I use [here](https://www.reddit.com/r/crowdstrike/comments/oz9oow/comment/h7z7wy8/?utm_source=reddit&utm_medium=web2x&context=3). If you want to view the file by itself, you use the following: | inputlookup lookuptable
