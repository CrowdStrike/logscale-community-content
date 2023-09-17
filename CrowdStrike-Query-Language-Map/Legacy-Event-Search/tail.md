Comments: In Legacy Event Search, the `tail` function is used to show a fixed number of the **oldest** events. Example:

```
event_simpleName=ProcessRollup2
| tail 5
```

In LogScale, the `head` and `tail` commands act as they would in Linux and Unix. For this reason, `tail` in LogScale will return a fixed number of the **most recent** events within the search window. Example:

```
#event_simpleName=ProcessRollup2
| tail(5)
```

[[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/tail|tail]]



