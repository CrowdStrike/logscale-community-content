```
#sampleType = repository
| timechart(repo,
function={sum(ingestAfterFieldRemovalSize)}, minSpan=1h, limit=20)
```