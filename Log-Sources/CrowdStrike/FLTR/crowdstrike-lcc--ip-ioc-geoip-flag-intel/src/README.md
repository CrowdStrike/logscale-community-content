This package is not a replacement for any comparable package from the [LogScale Package Marketplace](https://library.humio.com/humio-server/packages-marketplace.html). It is primarily used by the CrowdStrike SE team in POV implementations, however it can be used in Production implementations as well.

## Network Connections (IP) - IOC / Threat Actor / Geo
This package contains a dashboard and two saved searches that make use of the IOC Threat Intel and GeoIP mapping capabilities available in LogScale.

For more information about the "ioc:lookup()" query option: https://library.humio.com/data-analysis/functions-ioc-lookup.html

For more information about the "ipLocation()" query option: https://library.humio.com/data-analysis/functions-iplocation.html
 
## Package Contents
- Saved Searches
- Saved Dashboard
- Saved Geo mapping file (country names, continents, flag)
 
## Use Case
- SecOps
 
## Technology Vendor
CrowdStrike
 
## Dependencies
This package assumes the following:

- Network-based events (from CrowdStrike endpoints or other non-CrowdStrike sources) are being ingested

## Installation
Installing the package will automatically deploy the Network Connections (IP) - IOC / Threat Actor / Geo dashboard and saved searches. This is meant to be installed in a **view** across data (for example, Falcon telemetry data, firewall data, etc.), *not* a repo. 

Once installed:

- Update the "zIOC_traffic_field_normalization" saved search with your specific network traffic source information (specific events or repos, mapped into the source/destination IP standard field format listed)

- Within the "Network Connections (IP) - IOC / Threat Actor / Geo" saved search, and each of the widgets in the "Network Connections (IP) - IOC / Threat Actor / Geo" dashboard, update the "rootURL" section and comment in the CrowdStrike URL that applies to your region (and comment out the other three)

- To access the "IOC Actor Intel" field contents, first log in to your Falcon UI

- NOTE: Microsoft does not support flag emojis, so country codes will be displayed instead