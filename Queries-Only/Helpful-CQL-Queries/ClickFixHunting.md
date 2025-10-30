// Fleshed out query for clickfix detection

#event_simpleName=ProcessRollup2 
| #repo=base_sensor
| ParentBaseFileName=explorer.exe
| TargetProcessId=*
|in(field="FileName",ignoreCase=true, values=[
    *powershell*,*pwsh*,*cmd*,*mshta*,*wscript*,*cscript*,
    *rundll32*,*regsvr32*,*wmic*,*msbuild*,*installutil*,
    *bitsadmin*,*curl*,*ftp*,*hh*,*schtasks*,*certutil*
])
|in(field="CommandLine",ignoreCase=true, values=[
    *iex*,*irm*,*iwr*,*invoke-webrequest*,*http*,*https*,
    *ftp*,*smb*,*download*,*encodedcommand*,*bypass*,
    *invoke-expression*,*reflection.assembly*,*frombase64string*,
    *start-process*,*comobject*,*new-object*,*datetime*,*encoded*
])
| process_tree := format("[PT](/graphs/process-explorer/tree?_cid=%s&id=pid:%s:%s&investigate=true&pid=pid:%s:%s)", field=["#repo.cid","aid","TargetProcessId","aid","TargetProcessId"])
| groupBy([process_tree,ComputerName,ParentBaseFileName,FileName,CommandLine], limit=max)
