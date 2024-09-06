# AppOmni

Parser and a dashboard for AppOmni. Ingest SaaS application logs from AppOmni to LogScale or NG SIEM to detect and respond to suspicious activity such as highly privileged misconfigurations, configuration changes, unusual user behavior, and excessive consumption of data related to your SaaS ecosystem. AppOmni takes all your SaaS platforms audit logs and normalizes them into a modified ECS format. The tool then enriches logs with threat intelligence, and runs the data through the AppOmni threat detection rules to identify malicious sequence of events.

The AppOmni Alerts Dashboard for Crowdstrike provides a view of all your alerts, where you can see the severity distribution, geolocation, alerts over time, and any associated events. You can import it to NG SIEM through the dashboard import functionality. See [integrations page](https://library.humio.com/integrations-appomni-package-appomni) for more info on how to use AppOmni in LogScale and details about the parser.

See [AppOmni Developer Platform site](https://appomni.com/solutions/) for a comprehensive list of supported applications.

## Changelog

Version 0.2.0

- Updated the parser to set the `threat.*` fields
- Added new `AppOmni Events` dashboard

## Package Contents

### Parsers

- `AppOmni`

### Dashboards

- `AppOmni Alerts`
- `AppOmni Events`

## Use case

- SecOps

## Technology Vendor

Appomni

## Support

This package is supported by AppOmni. For any assistance with installing or using the package, please contact them by email at partners@appomni.com.

## Installation

For more complete installation instructions please look at our [integrations page](https://library.humio.com/integrations-appomni-package-appomni) for LogScale or contact your AppOmni account manager to get the steps involved to integrate it with CrowdStrike Next-Gen SIEM platform.
