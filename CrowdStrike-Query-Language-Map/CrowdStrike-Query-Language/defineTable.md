defineTable executes a subquery that generates an in-memory, ad-hoc table based on its results. The ad-hoc table can be joined with the results of the primary query using the [[match]] function.

```
defineTable(
    query={ #event_simpleName=ZipFileWritten
    }, include=[ContextProcessId,TargetFileName,aid],name="zip_file_writes")
| #event_simpleName=ProcessRollup2
| match(table="zip_file_writes",field=[aid, TargetProcessId], column=[aid, ContextProcessId])
| table([@timestamp,ComputerName,FileName, CommandLine, TargetFileName], limit=1000)
| rename([[FileName,WritingFile], [CommandLine, WritingCmdLine], [TargetFileName, WrittenFile]])
```

[defineTable documentation](https://library.humio.com/data-analysis/functions-definetable.html)
