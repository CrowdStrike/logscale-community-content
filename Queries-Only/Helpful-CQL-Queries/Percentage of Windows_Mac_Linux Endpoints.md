```
#event_simpleName=OsVersionInfo event_platform=/^(Win|Mac|Lin)$/

| groupBy(field=#cid, function=[count(aid, distinct=true, as=totalcount), {event_platform=Lin | count(aid, distinct=true, as=Linux)},{ event_platform=Mac | count(aid, distinct=true, as=Mac)}, { event_platform=Win | count(aid, distinct=true, as=Windows)}])
| linuxPercentage := (Linux/totalcount)*100 | format(format="%,.3f%%", field=[linuxPercentage], as=linuxPercentage)
| windowsPercentage := (Windows/totalcount)*100 | format(format="%,.3f%%", field=[windowsPercentage], as=windowsPercentage)
| macPercentage := (Mac/totalcount)*100 | format(format="%,.3f%%", field=[macPercentage], as=macPercentage)
| select([#cid, totalcount, Windows, windowsPercentage, Linux, linuxPercentage, Mac, macPercentage])

```