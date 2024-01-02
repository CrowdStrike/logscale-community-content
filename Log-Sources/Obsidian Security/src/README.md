## Obsidian Security

Obsidian cloud detection and response delivers unified visibility and protection across IaaS and SaaS environments. 

Security teams can get started with Obsidian in minutes with no software to deploy, and instantly get a view of access, privileges, and activity across cloud services. 

Obsidian connects to leading cloud services in minutes via API to aggregate data about access and activity. The platform normalizes and analyzes the data using built-in policies and behavior analytics to detect breaches, insider threats, access misuse, data exposure, excessive privileges, and misconfigurations.

This package contains a parser and 2 Dashboards 

Within the dashboard there are multiple searches/queries that can be used to visualise data ingested from Imperva's Cloud Web Application Firewall.

The Obsidian platform creates the following comprehensive and detailed logs:
- Posture and Compliance Alerts
- Threat Detection Alerts
- Integration Risk Alerts

Log integration mode recommended for this package:

Receive (Push mode): 
Log integration is achieved via Webhook. Obsidian Alerts are pushed to your designated LogScale repository by way of the LogScale Ingest API (https://library.humio.com/integrations/api-ingest.html#api-ingest-raw-data).
Refer to https://docs.obsidiansecurity.com/obsidian/settings/workflow-integrations/webhook-integrations/crowdstrike-falcon-logscale for further information.

## Release Notes

v0.1.0 
- Initial creation

v0.2.0 
- Updated parser with OpenTelemetry Data Model https://opentelemetry.io/docs/specs/otel/logs/data-model-appendix/#elastic-common-schema (ECS 8.11.0)

## Package Contents

- Parser
- Dashboards

## Use Case:

- SecOps

## Technology Vendor

Obsidian Security

## Support

Package creator doesn't currently offer support for this package.

## Dependencies

None

## Installation

Please refer to the following Obsidian Security Installation and Configuration guide - https://docs.obsidiansecurity.com/obsidian/settings/workflow-integrations/create-a-webhook-to-crowdstrike-falcon-logscale
