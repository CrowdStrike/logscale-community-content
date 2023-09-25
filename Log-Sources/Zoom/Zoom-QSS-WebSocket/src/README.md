# Zoom QSS QoS Telemetry
This package provide various LogScale assets necessary to parse, search, and visualize Zoom QSS QoS telemetry data.
This package includes (2) dashboards which provide an overview and breakdown of Zoom QSS event data.
These dashboards allow you to explore Zoom QoS data for operational troubleshooting and security use cases.

*Note:* This Package depends on a companion integration: [Zoom Qss LogScale integration](https://github.com/CrowdStrike/Zoom-QSS-WebSocket-Falcon-Logscale-Integration).

The Zoom Qss LogScale integration contains the Python3 code and supporting assets to establish a WebSocket connection to the Zoom QSS api, in order to receive QSS QoS events, and forward them to LogScale for ingest.

## Release Notes
v0.1.0 
- Initial release

## Package Contents

#### Parser
- `zoom_qss`

#### Actions
- `Connection Types` *(file upload)*
- `Network Types` *(file upload)*
- `Zoom Devices` *(file upload)*
- `Zoom Event Types` *(file upload)*
- `Zoom Version` *(file upload)*

#### Dashboards
- `QSS Overview` - A summary and high level view of Zoom meetings and webinars
- `Zoom Event Metrics` - A fuller view of Zoom events with the capability to inspect a specific meeting or webinar.

#### Lookup Files
- `county_codes__iso_3166.csv` - Country code to country name lookup file

#### Scheduled-Searches
- `Gather Connection Types`
- `Gather Network Types`
- `Collect Zoom Devices`
- `Zoom Event Types`
- `Gather Zoom Versions`

## Use Case
- DevOps
- SecOps

## Technology Vendor
Zoom

## Dependencies
- As noted above, this Package depends on a companion integration: [Zoom Qss LogScale integration](https://github.com/CrowdStrike/Zoom-QSS-WebSocket-Falcon-Logscale-Integration).


## Installation
1. If not previously created, create the Zoom QSS repository.
2. Install this package in the Zoom QSS repository.
3. Create an ingest token for the `zoom_qss` parser *(copy the token value)*. Assign the `zoom_qss` parser to the token.
4. Configure [Zoom QSS LogScale integration](https://github.com/CrowdStrike/Zoom-QSS-WebSocket-Falcon-Logscale-Integration) to send logs to LogScale
5. Verify that events are being ingested, and parsed by the `zoom_qss` parser

Once data begins streaming into the repository, the Zoom QSS LogScale dashboards will render the Zoom telemetry.