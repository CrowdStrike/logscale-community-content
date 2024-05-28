```

#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/.*\\powershell\.exe/

| CommandLine=/.*\s+\-(e|encoded|encodedcommand|enc)\s+.*/
| length("CommandLine", as="cmdLength")
| groupby([CommandLine], function=stats([collect(cmdLength), count(aid, distinct=true, as="uniqueEndpointCount"), count(aid, as="executionCount")]), limit=max)
| table([executionCount, uniqueEndpoitnCount, cmdLength, CommandLine])
| sort(executionCount, order=desc)

```
