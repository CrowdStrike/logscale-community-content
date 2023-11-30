# CrowdStrike Core FLTR Package

This package contains a robust set of content for use with Falcon Long Term Repository (FLTR). 

## Important

This package should be installed in a *view* linked to your FLTR repo. It is not necessary or recommended to install this directly into the FLTR repo. The FLTR *repo* should already have the additional `crowdstrike/fdr` package installed, which contains the parser necessary for this data.

If both packages are mistakenly installed in the FLTR repo, go to `Alerts -> Scheduled Searches -> FDR aidmaster Scheduled Search` and **uncheck** `Enable scheduled search` followed by `Save Scheduled Search`. Otherwise both packages will be attempting to generate the same file. You only need the `FLTR aidmaster Generation` scheduled search running. 

## Setup Instructions

Follow the [package setup instructions](https://github.com/CrowdStrike/logscale-community-content/wiki/FLTR-Setup-and-Configuration) to get going. It is highly recommended that you follow these steps after installing this package.

## Changelog

Version 1.3.9
- Reduced the CSV lookup generation to 24 hours with a 7-day lookback since `ComputerName` is now included in the FLTR data stream.
- Changed inputs to use `wildcard()` as needed. Input something like `*HTTP*` to find `http`, `HTTPS`, `HttPs`, etc.
- Minimum LogScale version increased to `1.103.0` to include filter alerts. 
- Made updates to data formatting in the queries. 
- Optimized dashboard queries related to detections.

Version 1.3.8
- Added the missing recon_apps.csv file and associated references. 

Version 1.3.7
- Changed the MITRE content to weigh the values around severity instead of just count. 
- Added "Search - Acquire Host Details" to the dashboards and interactions. 
- Added "Audit - Falcon UI Audit Logs" to monitor your Falcon audit logs from FLTR.
- Fixed a typo in the Linux health dashboard. 
- Bumped the minimum LogScale version to 1.96.0 to match released features.
- Added several example alerts. 

Version 1.3.6
- Enabled "Require user input before searching" for most of the dashboards. You can use `*` as an input if needed. 
- Enabled interactions for all dashboards where applicable. Clickable widgets!
- Renamed titles with "AID" to "AgentId" for consistency.
- Renamed "Inventory" and "File Vantage" dashboards for consistency. 
- Renamed the "Windows" dashboards to put them under the "OS" category. 
- Renamed a large number of saved queries to make the description more accurate. 
- Added a `zUsbNormalize()` user function to normalize USB events to human-readable names. 
- Added new queries from other internal packages.
- Bumps minimum required version of LogScale to 1.85.

Version 1.3.5
- Added the query name as a comment at the beginning of each query. 
- Dashboard fixes where groupBy value links were incorrect due to field renaming.
- Interactions for file hashes. 
- Query optimizations in a few places where the `default()` function is used. 
- Added additional optimizations to `zCommunityId`, which now includes detection events. 

Version 1.3.4
- Added a `zCommunityId` user function to calculate the Community Id.
- Added Event Interactions for ContextProcessId and TargetProcessId.
- Added a `Processes - Outbound Connections From a Process Name` query that is based on CVE-2023-23397.
- Dashboard updates for a future release of the FLTR parser. 
- Minor dashboard fix where the legend was missing. 

Version 1.3.3
- Initial public release. 

## Package Contents

### Dashboards

There is a selection of dashboards for getting quick value with FLTR. These may serve as the basis for building custom FLTR dashboards, alerts, and queries to match your specific use case.

### Queries

This package provides a wide range of saved queries. These can all be customized or used as a reference point for building additional queries. There is also a selection of user functions to assist with commonly used queries. 

### Event Interactions

Event interactions are included for both `aid` and `UserName` fields. This allows you to quickly pivot between the search and dashboard sections. 

### Schedules Searches

A scheduled search is included that generates the `fdr_aidmaster.csv` lookup file for matching the `aid` to `ComputerName` values. 

## Use Case

- SecOps

## Support

This package is supported by CrowdStrike. For any assistance with installing or using the package please contact us via the [support portal](https://www.crowdstrike.com/products/observability-and-log-management/support/), or by email at logscalesupport@crowdstrike.com.
