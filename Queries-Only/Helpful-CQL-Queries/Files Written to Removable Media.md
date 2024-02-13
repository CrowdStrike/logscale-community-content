```
event_platform=Win #event_simpleName=/Written/ IsOnRemovableDisk=1 
| FileSizeMB:=unit:convert(Size, to=M) 
| groupBy([ComputerName], function=([sum(Size, as=SizeBytes), sum(FileSizeMB, as=FileSizeMB), count(TargetFileName, as="File Count"), collect([TargetFileName])]))
```

```
#event_simpleName=/FileWritten$/ AND ((event_platform=Win DiskParentDeviceInstanceId="USB*") OR (event_platform=Mac IsOnRemovableDisk=1)) AND TargetFileName!="*.Spotlight-V100*"
| groupBy([ComputerName], function=([collect([TargetFileName]), count(TargetFileName, as=TotalFile), sum(Size, as=SumSize)]))
| TotalFiles > 10 OR SumSize > 5242880
| case {
    SumSize>=1099511627776 | Transfered:=unit:convert(SumSize, to=T) | format("%,.2f TB",field=["Transfered"], as="Transfered");
    SumSize>=1073741824 | Transfered:=unit:convert(SumSize, to=G) | format("%,.2f GB",field=["Transfered"], as="Transfered");
    SumSize>=1048576| Transfered:=unit:convert(SumSize, to=M) | format("%,.2f MB",field=["Transfered"], as="Transfered");
    SumSize>=1024 | Transfered:=unit:convert(SumSize, to=k) | format("%,.2f KB",field=["Transfered"], as="Transfered");
    * | Transfered:=format("%,.2f Bytes",field=["SumSize"]);
}
```