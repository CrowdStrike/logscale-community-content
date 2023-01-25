## Imperva Cloud Web Application Firewall
Web application attacks prevent important transactions and steal sensitive data. 
Imperva Web Application Firewall (WAF) stops these attacks with near-zero false positives and a global SOC to ensure your organization is protected from the latest attacks minutes after they are discovered in the wild.

This package contains a parser, three dashboards and two csv files. 

Within the dashboard there are multiple searches/queries that can be used to visualise data ingested from Imperva's Cloud Web Application Firewall.

Imperva creates the following comprehensive and detailed logs:
- Security logs
- Access logs

Log integration mode recommended for this package:

Receive (Push mode): 
Automatic log integration via Amazon S3. Your logs are pushed upon creation to your pre-defined repository - an AWS S3 bucket or an SFTP folder. Logs are automatically transferred from the Imperva cloud repository to your repository.
Refer to https://docs.imperva.com/bundle/cloud-application-security/page/settings/log-integration.htm for further information.

For more information on how Imperva can provide valuable data for your security operations please visit https://www.imperva.com/

## Release Notes

v0.1.0 
- Initial creation

v0.2.0 
- Change of dashboard names
- Tables changed to EventLists
- Minor SingleValue widget colour changes
- Removal of 'Security Events #2' Table Widget
- Redesign of Search Dashboard
- FQDN Parameter added to all dashboards

## Package Contents
## Parsers
- Imperva_ApplicationSecurity_CloudWebApplicationFirewall_cef

## Dashboards
- Account Overview
- Search
- WAF Overview

## Use Case:
- SecOps

## Technology Vendor:
Imperva

## Support
Package creator doesn't currently offer support for this package.

## Dependencies
The package uses logs from the following log type: CEF

Please make sure unencrypted CEF is selected when configuring the log forwarding from Imperva.

Package uses 2 files for country code matching and severity level which included within the package.

## Installation
The preferred option for sending logs from Imperva to LogScale is to choose Amazon S3 (available under 'Account Management' in the Imperva CWAF Console). 
Log Shipping from S3 to LogScale can be done in multiple ways, please see the LogScale documentation to ensure the right option is selected for you.

Please ensure logs are using the package parser 'cef' and the correct LogScale token is chosen.


