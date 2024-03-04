# Google Chrome Enterprise Logs

___Breaking changes warning___

_This update includes parser changes, which means that data ingested after upgrade will not be backwards compatible with logs ingested with 0.1.5.
Updating to version 0.2.0 or newer will therefore result in issues with dashboard widgets and queries created prior to 0.2.0._

Organizations are now able to get additional visibility into managed Google Chrome Enterprise Browsers and Devices using LogScale and Google's Chrome Enterprise Connector Framework. This package can be used to parse incoming event data making it searchable in LogScale. The package includes dashboards which give different breakdowns of events, for both Chrome and ChromeOS. These dashboards help get you started and exploring this valuable data source for security professionals.

## Changelog

Version 0.2.0

- Introducing a new dashboard: ChromeOS Data Controls
- Adapted the parser to be compliant to a common schema based on an [OpenTelemetry standard](https://opentelemetry.io/docs/specs/otel/logs/data-model-appendix/#elastic-common-schema).
- Added a widget for Chrome Browser crash events in the Event Information Dashboard
- Added additional columns to the Events widget of the Event Information Dashboard to include Crowdstrike Customer ID and Agent ID

Version 0.1.5

- Introduces 2 new dashboards: Extension Monitoring and ChromeOS Overview.
- Includes additional widgets for new Google Chrome Enterprise Events, such as Chrome Remote Desktop (CRD) and Password Reuse Events.
- Reorganized widgets within the Security Overview for better visibility of notable events.
- Added parameters to dashboards to aid pivoting on key values.
- Bumps the minimum supported version of LogScale to 1.82

## Package Contents

### Parser

- Google_Chrome_Enterprise

### Dashboards

- Security Overview - A summary and high level breakdown of key security events
- Event Information - A fuller view of all logs with ability to filter and time charts showing event volumes over time
- Extension Monitoring - A quick view to monitor extension installations for Chrome Browsers and ChromeOS
- ChromeOS Overview - An overview for ChromeOS specific security events including logons, USB Drive logs, and Chrome Remote Desktop (CRD) usage
- ChromeOS Data Controls - An overview for ChromeOS Data Controls allowing to enable visibility to protect users from data leakage on endpoints 

## Use Case

- SecOps
- ITOps

## Technology Vendor

Google

## Support

This package is supported by CrowdStrike. For any assistance with installing or using the package, please contact us via the [support portal](https://www.crowdstrike.com/products/observability-and-log-management/support/) or by email at logscalesupport@crowdstrike.com.

## Dependencies

To facilitate this organizations will need a cloud managed Chrome browser or Chrome device and to connect the data feed to LogScale's HEC endpoint API as described here: [Configuring Google Chrome Enterprise Connector](https://support.google.com/chrome/a/answer/11375053)

## Installation

This is a quick introduction to getting started with the package. For detailed instructions on setting things up, please see the [LogScale Library](https://library.humio.com/humio-server/integrations-google-chrome-enterprise.html).

1. Install this package in the relevant repository and create a new ingest token for the Google_Chrome_Enterprise parser and copy this token value. Assign the parser from this package to the token.
2. Configure Google Chrome Enterprise Connector Framework to send logs to LogScale
3. (Optional) Add blocklisted/unwanted Chome Browser Extensions to the lookup file "chrome_extensions_blocklist.csv" with the column name "extension_id" for the "Blocklisted Extension Installed" widget in the "Chrome Enterprise Security Extension Dashboard". Values for the "extension_id" column are the unique ID of the extension from the Chrome web store. The ID can be found in the URL of the extension in the Chrome web store. Eg: "kchfmpdcejfkipopnolndinkeoipnoia" for "User-Agent Switcher"

You should now see the LogScale dashboards begin to populate and can start searching the data.
You can read up on the different [Chrome Enterprise events here](https://support.google.com/a/answer/9393909?hl=en).