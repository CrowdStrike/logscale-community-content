

This package is not a replacement for the [LogScale Package Marketplace](https://library.humio.com/humio-server/packages-marketplace.html). It is primarily used by the CrowdStrike SE team as learning examples. 

## CrowdStrike Falcon Identity Protection
This package contains dashboards and saved searches that highlight Falcon Identity Protection detections as well as identity telemetry events. For more information on the CrowdStrike Falcon Identity Protection, please visit the following:

https://www.crowdstrike.com/products/identity-protection/falcon-identity-threat-detection/
 
## Package Contents
- Saved Searches
- Saved Dashboards
 
## Use Case
- SecOps
 
## Technology Vendor
CrowdStrike
 
## Dependencies
This package assumes the following:

- CrowdStrike FDR parser has been installed.
- CrowdStrike Falcon Identity Protection is being sent to LogScale.

## Installation
Installing the package will automatically deploy the Falcon Identity Protection dashboards and saved searches. This is meant to be installed in a **view** of the Falcon telemetry data, *not* the repo. 