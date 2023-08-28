# Armis Package for Humio
This Armis package can be used to parse incoming logs from Armis via HTTP Event Collection (HEC).

## Package Contents
- Parsers
    - 1 Parser for data being ingested into the Humio repository
- Dashboards
    - Alert Overview

## Use Case
- SecOps

## Technology Vendor
Armis

## Support
CrowdStrike Integrations maintains and supports this integration. Please create a [Support Ticket](https://supportportal.crowdstrike.com ) with any issues.

## Dependencies
- Produciton Armis Platform
- HEC log output configured in Armis (Armis &rarr; Integrations &rarr; SIEM &rarr; Configure Humio details and choose "Splunk HTTP/S" as the connection type)

## Installation
Installation of the package is straightforward, the installation will deploy the parser, saved queries, and dashboards directly into the repository you install the package into.

Once installed, select the <armis> parser as the default for the Repository Ingestion Token.  Use that token when configuring the Armis SIEM integration within the Armis Platform. 