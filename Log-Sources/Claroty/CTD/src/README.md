# Claroty CTD Package for LogScale
This package can be used to parse incoming Claroty CTD CEF formatted logs via HTTP Event Collection (HEC).

## Package Contents
- Dashboards
    - CTD Alerts
    - CTD Events
    - CTD Health
    
## Technology Vendor
Claroty

## Support
CrowdStrike Integrations maintains and supports this integration. Please create a [Support Ticket](https://supportportal.crowdstrike.com ) with any issues.

## Dependencies
- Produciton Claroty CTD Platform
- CEF log output configured in Claroty CTD 
- Log collector to ingest syslog CEF from Claroty CTD and output in HEC format to LogScale. Possible log collectors include:
    - LogScale Log Collector
    - Syslog-ng

## Installation
Installation of the package will deploy the parser, saved queries, and dashboards directly into the selected repository.

The Ingest Token of the Repository will be used to configure the log collector to send logs via HEC to LogScale.