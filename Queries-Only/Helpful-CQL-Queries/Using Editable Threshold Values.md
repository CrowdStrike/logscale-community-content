```
#event_simpleName=ProcessRollup2 ImageFileName=/(\\|\/)whoami/i
| groupBy([aid], function=(count(aid, as=executionCount)))
| myThreshold:=?myThreshold
| myThreshold:=if(condition=(myThreshold == "*"), then="0", else=myThreshold)
| test(executionCount>myThreshold)
```