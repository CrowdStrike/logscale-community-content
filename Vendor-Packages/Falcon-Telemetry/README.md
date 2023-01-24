:warning: These are unofficial packages. :warning:

These are packages used by the LogScale SE team during POVs. They are not meant to be a replacement for the official LogScale [Package Marketplace](https://library.humio.com/humio-server/packages-marketplace.html). However, feel free to use the content as necessary since they are meant to be learning examples. 

The packages generally include much more content than [individual dashboards, queries, alerts, etc](LogScale-and-FLTR/Vendor-Content). 

- **[falcondata-idp](falcondata-idp)**: queries and dashboards for Falcon Identity Threat Detection in LogScale. 
- **[falcondata-greenfield](falcondata-greenfield)**: queries and dashboards for Falcon telemetry, aka FDR. This must be installed with the [falcondata-zen](falcondata-zen) package.
- **[falcondata-zen](falcondata-zen)**: scheduled searches and user functions that act as the underpinning for the [falcondata-greenfield](falcondata-greenfield) package.
- **[falcondata-parser](falcondata-parser)**: a stand-alone parser for Falcon telemetry, aka FDR. You likely do not need this. 