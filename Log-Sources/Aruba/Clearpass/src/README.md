
# README
## Aruba Clearpass
This package is work in progress, but it works as is!

## Package Contents
* Parser
* Dashboards
* Enrichment file for Clearpass event codes
## Use Case
* SecOps
## Technology Vendor
[Aruba Networks](https://www.arubanetworks.com/products/security/network-access-control/secure-access/)

## Support
...

## Dependencies
None

## Installation
Configure Clearpass to send events via syslog in LEEF format.
For more information see [Clearpass documentation](https://www.arubanetworks.com/techdocs/ClearPass/6.8/PolicyManager/Content/CPPM_UserGuide/Admin/syslogExportFilters_add_syslog_filter_general.htm)
Collect the events with the Falcon LogScale Collector.
