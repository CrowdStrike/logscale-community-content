## CrowdStrike Falcon Device Control
This package contains dashboards that highlight Falcon Device Control events. For more information on the CrowdStrike Device Control, please visit the following:

https://www.crowdstrike.com/products/endpoint-security/falcon-device-control/

## Dependencies
- The `crowdstrike/fltr-core` package must be installed in the same view as this package. 
 
## Changelog
Version 0.1.1
- Query optimizations. 
- `wildcard()` all the things!

Version 0.1.0
- Initial release. 

## Package Contents
- Saved Dashboards

## Use Case
- SecOps
 
## Technology Vendor
CrowdStrike
 
## Dependencies
This package assumes the following:

- CrowdStrike FDR parser has been installed.
- CrowdStrike Falcon Device Control is being sent to LogScale.

## Installation
Installing the package will automatically deploy the Falcon Device Control dashboards. This is meant to be installed in a **view** of the Falcon telemetry data, *not* the repo. 