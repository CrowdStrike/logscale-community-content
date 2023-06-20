## Microsoft DNS Log File Parser

The purpose of this file is to enable the parsing of the Windows DNS log file that was created on disk by the service. 
The DNS log file format is a single string of text with spaces and specific codes in certain spaces and contains a carriage return between each log line.

Underneath the title there should be a description of what it does and why. Focus on what log sources does it apply to, what data does it use and what does it show from that data. Make it really clear as to what the purpose of the package is.You can include links to external websites as long as they are directly relevant and help explain the package or add context. You can include links to Humio's documentation library to explain concepts and provide technical details or helpful tips.

## Release Notes

v0.1.0 
- Initial creation

## Package Contents

- Parser

## Use Case:

- SecOps - useful for security operations teams, typically to provide security monitoring and SIEM like functionality.

- ITOps - used by IT operations teams to monitor IT systems and to provide investigations and root cause analysis

## Technology Vendor

Microsoft Active Directory DNS

## Support

Package creator doesn't currently offer support for this package.

## Dependencies

- CAUTION - Using debug logging options slows DNS server performance. For this reason, all debug logging options are disabled by default.
- CAUTION - Debug logging can be resource intensive, affecting overall server performance and consuming disk space. Therefore, it should only be used temporarily when more detailed information about server performance is needed.

Enable Debug Logging: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc759581(v=ws.10)

More on Debug Logging Options: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc776361(v=ws.10)?redirectedfrom=MSDN

After debug logging is enabled, the log file must be tailed and shipped to LogScale. Here is an example logscale collector config file that can be used to tail and ship the log:

https://github.com/CrowdStrike/logscale-community-content/blob/main/Config-Samples/Log-Shippers/Falcon-LogScale-Collector/FLC-Standalone-BasicWindowsEventsAndLogFileconfig

The following section will need to be updated: The path to the dns log file from the steps above and the specific parser that will parse this log file (which is the related parser of this project)

This section identifies a log file on disk to be tailed and shipped.
```
sample_log:
  type: file
  include: C:\SAMPLELogPath\SAMPLELogFile.log
  sink: humio
```

This configuration file sample sets a custom parser for the log file that you are shipping. If you use a parser in the yaml file then set the ingester parser to none.

parser: SAMPLECUSTOMPARSER

## Installation

- Import/Create the parser 
- Review the parser settings, it is configured to drop some fields that may or may not be required for your current needs.

Install the Falcon LogScale Collector on the target host and modify the config.yaml as required:

- Update the file path.
- Update the parser name (it's currently named 'msdnslog') in the log collector .yaml file that is referenced above. 

Follow all other instructions required to ingest data from a log collector.
