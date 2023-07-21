# Kubernetes Logging

This package provide dashboards, saved searches, actions, and a parser for observing kubernetes cluster operations.

The dashboards provide visualizations for kubernetes logs and cluster node system metrics.
The saved searches and actions are used to create the lookup tables used by dashboard parameters.

Dashboards and saved searches in this package assume the presence field enrichments added by the fluent-bit log shipper (fluentbit.io).  Please see installation notes below for details regarding the fluent-bit log shipper..

## Package Contents

Parser:

- Built-in *json* parser

Dashboards:

- Audit Events
- Kubelet Logs
- Kubernetes Container Search
- Kubernetes Control-Plane Summary
- Docker Events
- CPU Metrics
- Network Metrics
- Disk Metrics
- Memory Metrics

Scheduled Searches:

- Kubelet Go Modules
- Kubernetes Cluster Hostnames
- Kubernetes Container Actions
- Kubernetes Network Interfaces
- Kubernetes Pod Names Lookup

Actions:

- Kublet Go Modules Lookup (*Upload file*)
- Kubernetes Cluster Hostnames Lookup (*Upload file*)
- Kubernetes Container Actions Lookup (*Upload file*)
- Kubernetes Network Interfaces Lookup (*Upload file*)
- Kubernetes Pod Names Lookup (*Upload file*)

## Use Cases

- SecOps
- ITOps
- DevOps

## Technology Vendor

Kubernetes (kubernetes.io)

## Support

This package is supported by our product support team. If you have any issues implementing or running this package, please visit support.humio.com for assistance.

## Dependencies

- Fluent-Bit (fluentbit.io) log shipper

## Installation

1) Install this package in the relevant repository, and optionally create a new ingest token.
2) Assign the JSON ingest parser to the ingest token.
3) Configure the FluentBit log shipper to send logs and metrics to LogScale.

## Notes

### Fluent-Bit

Refer to the companion fluent-bit integration -- available on Crowdstrike GitHub -- for detailed configuration of fluent-bit log and metrics ingestions, and custom fields definitions expected by dashboard searches.

### Dashboards

These dashboards provide regular expression (regex) parameter search filtering:

- Kubelet Logs
- Kubernetes Container Search
- Kubernetes Control-Plane Summary

The default regex parameter value (blank) matching all events, is equavalent to (.*)