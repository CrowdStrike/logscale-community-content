## Package Name

This should be the name of the package but may include a couple of extra words if it help provide a meaningful title, must be less than 40 characters).

Underneath the title there should be a description of what it does and why. Focus on what log sources does it apply to, what data does it use and what does it show from that data. Make it really clear as to what the purpose of the package is.You can include links to external websites as long as they are directly relevant and help explain the package or add context. You can include links to Humio's documentation library to explain concepts and provide technical details or helpful tips.

## Release Notes

v0.1.0 
- Initial creation

## Package Contents

List which of below are included. (you can include a description of each component if you wish but limited to 100 characters each. All packages need to include the required parsers. This may change in the future but for now a working parser must be included (it can be subject to dependencies as listed in the dependencies section below).

- Parser
- Queries
- Alerts
- Dashboards

## Use Case:

(list all that apply from the selection of DevOps, SecOps, ITOps, IoT/OT)

- DevOps - used by devops teams to provide observability of applications and the platforms the code runs on, including containerised and micro-services type environments.

- SecOps - useful for security operations teams, typically to provide security monitoring and SIEM like functionality.

- ITOps - used by IT operations teams to monitor IT systems and to provide investigations and root cause analysis

- IoT/OT - used to provide security and/or operational management of Internet of Things devices or Operational Technology such as Scada and industrial process control and monitoring.

## Technology Vendor

(list of vendors supported by package) e.g. AWS (Amazon Web Services) or Cisco.

## Support

Package creator doesn't currently offer support for this package.

## Dependencies

List/describe dependencies for your package to work. These will typically include versions or configurations of the log sources and often the log collection method and formatting of logs. You can include a sample line of log data to illustrate the required format.

## Installation

Instructions on how to ingest the data and how to install and use the package. Must include any required configuration in external systems such as log sources as well as explaining any optional configurations or choices that need to be made. These should be summary instructions with a link to the Humio documentation library and the specific integration step by step instructions.

If your package is a collection of template files for a specific technology, a short description is usually enough.

If your package is an application, it should also explain:

Any additional pre- or post-installation steps users need to take.

A general introduction about how to get started, e.g. including configuration files.