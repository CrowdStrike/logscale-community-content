Comments: In Legacy Event Search, the `head` function is used to show a fixed number of the **most recent** events. Example:

```
event_simpleName=ProcessRollup2
| head 5
```

In LogScale, the `head` and `tail` commands act as they would when interacting with a log file in Linux and Unix. For this reason, `head` in LogScale will return a fixed number of the **oldest** events within the search window. Example:

```
#event_simpleName=ProcessRollup2
| head(5)
```

To get the **most recent** events, use [[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/tail|tail]].

[[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/head|head]]


