```
//Get PowerShell Events
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\powershell\.exe/i
//Look for PS flags that indicate an encoded command
| CommandLine=/\s+\-(e|encoded|encodedcommand|enc)\s+/i
//Shorten ImageFileName to fileName
| ImageFileName=/\\(?<fileName>powershell\.exe$)/i
//Capture encoded flag used
| CommandLine=/\-(?<psEncFlag>(e|encoded|encodedcommand|enc))\s+/i
//Calculate commandline length
| length("CommandLine", as="cmdLength")
//Group by command frequency
| groupby([fileName, psEncFlag, cmdLength, CommandLine], function=stats([count(aid, distinct=true, as="uniqueEndpointCount"), count(aid, as="executionCount")]), limit=max)
| table([fileName, executionCount, uniqueEndpointCount, psEncFlag, cmdLength, CommandLine])
//Capture commandline prefix and encoded command blob
| CommandLine=/(?<cmdLinePrefix>.*)\s+(?<b64String>\S+$)/i
//Decode encoded command blob
| decodedCommand := base64Decode(b64String, charset="UTF-16LE")
//Calculate Shannon Entropy
| b64ShannonEntropy := shannonEntropy(b64String)
//Look for http(s) string
| decodedCommand=/https?\:\/\//i
| table([fileName, b64ShannonEntropy, psEncFlag, cmdLength, stdDevCmdLength, executionCount, uniqueEndpointCount, decodedCommand, b64String])
| sort(field=b64ShannonEntropy, order=desc)

```

OR

```

#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/.*\\powershell\.exe/
| CommandLine=/\s+\-(e|encoded|encodedcommand|enc)\s+/i
| CommandLine=/\-(?<psEncFlag>(e|encoded|encodedcommand|enc))\s+/i
| length("CommandLine", as="cmdLength")
| groupby([psEncFlag, cmdLength, CommandLine], function=stats([count(aid, distinct=true, as="uniqueEndpointCount"), count(aid, as="executionCount")]), limit=max)
| EncodedString := splitString(field=CommandLine, by="-e* ", index=1)
| CmdLinePrefix := splitString(field=CommandLine, by="-e* ", index=0)
| DecodedString := base64Decode(EncodedString, charset="UTF-16LE")
// Look for encoded messages in the decoded message and decode those too.
| case {
    DecodedString = /encoded/i
    | SubEncodedString := splitString(field=DecodedString, by="-EncodedCommand ", index=1)
    | SubCmdLinePrefix := splitString(field=EncodedString, by="-EncodedCommand ", index=0)
    | SubDecodedString := base64Decode(SubEncodedString, charset="UTF-16LE");
    *
}
| table([executionCount, uniqueEndpoitnCount, cmdLength, DecodedString, CommandLine])
| sort(executionCount, type=any, order=desc)

```

OR

```
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/.*\\powershell\.exe/
| CommandLine=/.*\s+\-(e|encoded|encodedcommand|enc)\s+.*/
| length("CommandLine", as="cmdLength")
| groupby([CommandLine], function=stats([count(aid, distinct=true, as="uniqueEndpointCount"), count(aid, as="executionCount")]), limit=max)
| EncodedString := splitString(field=CommandLine, by="-e* ", index=1)
| CmdLinePrefix := splitString(field=CommandLine, by="-e* ", index=0)
| DecodedString := base64Decode(EncodedString, charset="UTF-16LE")
// Look for encoded messages in the decoded message and decode those too.
| case {
    DecodedString = /encoded/i
    | SubEncodedString := splitString(field=DecodedString, by="-EncodedCommand ", index=1)
    | SubCmdLinePrefix := splitString(field=EncodedString, by="-EncodedCommand ", index=0)
    | SubDecodedString := base64Decode(SubEncodedString, charset="UTF-16LE");
    *
}
| DecodedString=/.*https?\:\/\/.*/
| table([executionCount, uniqueEndpoitnCount, DecodedString, CommandLine])
| sort(executionCount, type=any, order=desc)

```