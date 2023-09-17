Comments: In Legacy Event Search, the function `timechart` is used to graph or display search results in a time-centric manner. Example:

```
event_platform=Win event_simpleName=ProcessRollup2 FileName IN (chrome.exe, firefox.exe, msedge.exe)
|  timechart span=1d dc(aid) as uniqueEndpoints by FileName
```

In LogScale:

```
event_platform=Win #event_simpleName=ProcessRollup2 ImageFileName=/\\(?<FileName>(chrome|firefox|msedge)\.exe$)/
| timeChart(FileName, function=count(aid, distinct=true),span=1d)
```

Note: LogScale will default to the visualization view. You can switch to the tabular view by selecting the "Data" tab. 

[[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/timeChart|timeChart]]


