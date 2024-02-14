```
#event_simpleName=ScriptControlScanInfo event_platform=Win

| ScriptContent=/FromBase64String/i
| entropy := shannonEntropy("ScriptContent")
| groupBy([ScriptContent], function=([collect(entropy), count(ScriptContent, as=appearenceCount), count(aid, distinct=true, as=endpointCount)]))
| table([entropy, endpointCount, appearenceCount, ScriptContent])

//| entropy > 4.5 AND endpointCount =1 AND appearenceCount < 5

| sort(field=entropy, order=desc)

```