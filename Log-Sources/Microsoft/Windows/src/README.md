## Windows Security Overview
Windows Security logs are one of the pivotal data sources in a Security operations program.

This package contains a parser, five dashboards and three csv files.

Within the dashboard there are multiple searches/queries that can be used to visualise data ingested from Windows Logs

The main focus of these dashboards are data coming from Security Logs, however additional context will be displayed from collecting other channels as well:
- Security logs
- Application Logs
- System Logs
- Powershell
- etc..


## Release Notes

v0.1.0 
- Initial creation


## Package Contents
## Parsers
- windows

## Dashboards
- Windows Authentication Failure Activity
- Windows Group Management
- Windows Overview
- Windows Process Investigation
- Windows User Activity

## Use Case:
- SecOps

## Technology Vendor:
Microsoft

## Support
Package creator doesn't currently offer support for this package.

## Dependencies
This package was developed from Windows logs being natively collected by the LogScale Collector.

## Installation
1. Download and save the windows--overview_pack--$VERSION.zip.
2. Go to Settings → Installed → Import Package.
3. Browse to the windows--overview_pack--$VERSION zip file and install the package.
4. Please ensure logs are using the package parser 'windows' and the correct LogScale token is chosen.
5. Each of these dashboards has links embedded to quickly navigate back and forth between the other dashboards in this package. At this time, these links need to be configured manually for each repo/view this package is installed on. The quickest way to accomplish this is import the package and then navigate to one of the dashboards and then Edit, Go to the Links Widget and replace the link with each dashboards respective link. You'll need to have each dashboard open in its own tab and only grab and paste everything after the customer URL.  Example:  [System Overview](/General_Purpose_Lab_Data/dashboards/P0Gnc4vRHCkcFdoIhTiOs5ezr7izR670) Replace General_Purpose_Lab_Data/dashboards/P0Gnc4vRHCkcFdoIhTiOs5ezr7izR670 with everything past your root url. https://mylogscale.com/WindowsLogs/dashboards/JPIJLKSJF3r3sdfsdfds3453sdfsdDSFSD   /WindowsLogs/dashboards/JPIJLKSJF3r3sdfsdfds3453sdfsdDSFSD. Do this for each dashboard in the Links widget, copy all of the code in this widget and paste into the links widget on each dashboard. 


     