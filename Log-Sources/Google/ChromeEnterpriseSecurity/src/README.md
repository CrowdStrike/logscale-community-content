# Google Chrome Enterprise Logs
Organizations are now able to get additional visibility into managed Google Chrome Enterprise Browsers and Devices using LogScale and Google's Chrome Enterprise Connector Framework. This package can be used to parse incoming event data making it searchable in LogScale.  The package includes four sets of dashboards which provide an overview and breakdown of important security events, in ChromeOS as well as the Chrome browser, a view of all events with custom filters, as well as breakdowns of events by type and how they vary over time.  These dashboards help get you started and exploring this valuable data source for security professionals.

## Package Contents
#### Parser
- Google_Chrome_Enterprise
#### Dashboards
- Security Overview - A summary and high level breakdown of key security events
- Event Information - A fuller view of all logs with ability to filter and time charts showing event volumes over time
- Extension Monitoring - A quick view to monitor extension installations for Chrome Browsers and ChromeOS
- ChromeOS Overview - An overview for ChromeOS specific security events including logons, USB Drive logs, and Chrome Remote Desktop (CRD) usage


## Use Case
- SecOps
- DevOps

## Technology Vendor
Google

## Support
Supported by LogScale https://support.humio.com/

## Dependencies
To facilitate this organizations will need a cloud managed Chrome browser or Chrome device and to connect the data feed to LogScale's HEC endpoint API as described here: [Configuring Google Chrome Enterprise Connector](https://support.google.com/chrome/a/answer/11375053)

## Installation
This is a quick introduction to getting started with the package. For detailed instructions on setting things up, please see the [LogScale Library](https://library.humio.com/humio-server/integrations-google-chrome-enterprise.html).

1. Install this package in the relevant repository and create a new ingest token for the Google_Chrome_Enterprise parser and copy this token value. Assign the parser from this package to the token.
2. Configure Google Chrome Enterprise Connector Framework to send logs to LogScale
3. (Optional) Add blocklisted/unwanted Chome Browser Extensions to the lookup file "chrome_extensions_blocklist.csv" with the column name "extension_id" for the "Blocklisted Extension Installed" widget in the "Chrome Enterprise Security Extension Dashboard". Values for the "extension_id" column are the unique ID of the extension from the Chrome web store. The ID can be found in the URL of the extension in the Chrome web store. Eg: "kchfmpdcejfkipopnolndinkeoipnoia" for "User-Agent Switcher"

You should now see the LogScale dashboards begin to populate and can start searching the data.
More information about the different event types can be found here: [Google Chrome Enterprise Events](https://support.google.com/a/answer/9393909?hl=en)