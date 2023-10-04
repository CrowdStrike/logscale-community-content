# Kubernetes Fluent-Bit Logging
This LogScale package provide various assets necessary to parse, search, and visualize Kubernetes logging data that has been forwarded by the fluent-bit log shipper.

*Note:* This Package depends on the companion integration: [Fluent-Bit Logging LogScale Integration](https://github.com/CrowdStrike/Kubernetes-FluentBit-Logging-Falcon-Logscale-Integration).

Included are ten (10) dashboards which provide visibility into internal Kubernetes cluster operation, and application logging. Additionally, four (4) metrics dashboards provide node level visibility of device metrics for cpu, disk, memory, and network interfaces.

This package will allow you to explore Kubernetes logging data for operational troubleshooting and security use cases.


## Release Notes
v0.1.0 
- Initial release

## Package Contents

#### Parser
- `fluentbit`

#### Actions
- `Kubernetes Cluster Hostnames Lookup` *(file upload)*
- `Kubernetes Container Actions Lookup` *(file upload)*
- `Kubernetes Network Interfaces Lookup` *(file upload)*

#### Dashboards
- `Kubernetes Daemons` - Overview of Kubernetes system daemons
- `Kubernetes Events` - Overview of Kubernetes events
- `Kubernetes Container Search` - Overview of Kubernetes containers
- `Kubernetes Control-Plane Summary` - Overview of Kubernetes control-plane
- `Audit Events` - Overview of Kubernetes audit events
- `Docker Events` - Overview of Docker events
- `CPU Metrics` - Overview of node cpu metrics
- `Disk Metrics` - Overview of node disk metrics
- `Memory Metrics` - Overview of node memory metrics
- `Network Metrics` - Overview of node network metrics

#### Scheduled-Searches
- `Collect Kubernetes Cluster Hostnames`
- `Collect Kubernetes Container Actions`
- `Collect Kubernetes Network Interfaces`

## Use Case
- DevOps
- SecOps

## Technology Vendor
Kubernetes, Fluent-Bit

## Dependencies
- As noted above, this Package depends on a companion integration: [Fluent-Bit Logging LogScale Integration](https://github.com/CrowdStrike/Kubernetes-FluentBit-Logging-Falcon-Logscale-Integration)


## Installation
1. If not previously created, create the kubernetes-fluent-bit-logging repository.
2. Install this package in the kubernetes-fluent-bit-logging repository.
3. Create an ingest token for the `fluentbit` parser *(copy the token value)*. Assign the `fluentbit` parser to the token.
4. Configure the [Fluent-Bit Logging LogScale Integration](https://github.com/CrowdStrike/Kubernetes-FluentBit-Logging-Falcon-Logscale-Integration) to send logs to LogScale.
*The Fluent-Bit Logging LogScale Integration contains the instructions and configuration templates needed to setup and configure Fluent-Bit/Kubernetes log processing for forwarding to LogScale.*
6. Verify that events are being ingested, and parsed by the `fluentbit` parser.

Once data begins streaming into the repository, the Kubernetes/Fluent-Bit LogScale dashboards will render the Kubernetes/Fluent-Bit logging telemetry.
