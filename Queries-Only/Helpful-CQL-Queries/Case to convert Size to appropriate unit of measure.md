```
#event_simpleName=/FileWritten$/ 
| case {
    Size>=1099511627776 | CommonSize:=unit:convert(Size, to=T) | format("%,.2f TB",field=["CommonSize"], as="CommonSize");
    Size>=1073741824 | CommonSize:=unit:convert(Size, to=G) | format("%,.2f GB",field=["CommonSize"], as="CommonSize");
    Size>=1048576| CommonSize:=unit:convert(Size, to=M) | format("%,.2f MB",field=["CommonSize"], as="CommonSize");
    Size>1024 | CommonSize:=unit:convert(Size, to=k) | format("%,.3f KB",field=["CommonSize"], as="CommonSize");
    * | CommonSize:=format("%,.0f Bytes",field=["Size"]);
}
| table([@timestamp, aid, ComputerName, FileName, Size, CommonSize])
```