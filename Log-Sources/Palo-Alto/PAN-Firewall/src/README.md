
# Palo Alto Firewall Logs
Now Palo Alto Firewall Logs can be ingested into Falcon LogScale.  This package can be used to parse incoming log events making it searchable in Falcon LogScale.  The package includes sets of dashboards which provide an overview and breakdown of important firewall events, a view of all events with custom filters, as well as breakdowns of events by type and how they vary over time.  

## Package Contents
#### Parser
- Palo Alto Firewall log parser
#### Dashboards
- Data Transmission Ratio by Source/Destination IPs
- External Traffic by Action & Geo location
- Metrics Dashboard
- Summary Dashboard

## Use Case
- SecOps

## Technology Vendor
Palo Alto Networks

## Support
Supported by CrowdStrike https://support.crowdstrike.com/

## Dependencies
This can be done either sending firewall logs direcly or using Panorama. Panorama can send its own logs and can forward logs from firewalls to Falcon Logscale.[Configuring Syslog Monitoring ](https://docs.paloaltonetworks.com/pan-os/8-1/pan-os-admin/monitoring/use-syslog-for-monitoring/configure-s    yslog-monitoring)
## Installation

1. Install this package in the relevant repository and create a new ingest token for the Palo Alto Firewall logs parser and copy this token value. Assign the parser from this package to the token.
2. Configure the firewall to send logs to Falcon LogScale.

You should now see the Falcon LogScale dashboards begin to populate and can start searching the data.
More information about the different event types & fields can be found here: [Syslog Field Descriptions](https://docs.paloaltonetworks.com/pan-os/10-1/pan-os-admin/monitoring/use-syslog-for-monitoring/syslog-field-descriptions)
