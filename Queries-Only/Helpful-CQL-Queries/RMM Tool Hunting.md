```
#event_simpleName=ProcessRollup2 event_platform=Win
// Add in additional program names here.
| in(field="FileName", values=[anydesk.exe, AteraAgent.exe, teamviewer.exe, SRService.exe, SRManager.exe, SRServer.exe, SRAgent.exe, ClientService.exe, "ScreenConnect.WindowsClient.exe", ngrok.exe], ignoreCase=true)
| FilePath=/\\Device\\HarddiskVolume\d\\(?<ShortFilePath>.+$)/
| groupBy([FileName, ShortFilePath, SHA256HashData], function=([count(aid, as=TotalExecutions), count(aid, distinct=true, as=UniqueEndpoints), collect([ComputerName])]))
// Adjust threshold
| UniqueEndpoints<15
```