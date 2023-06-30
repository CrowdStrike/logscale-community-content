# Cisco ASA  Logs
Use the Cisco Secure Firewall ASA package to parse incoming firewall log events so that it's easier to query them in Falcon LogScale. This package also includes visualizations that help you monitor network traffic, and incorporates IOC intelligence to enhance the organization's security posture and incident response capabilities. Using IOC visual representation in LogScale dashboards helps you identify trends and patterns, aiding in the understanding and mitigation of threats. This package also includes a traffic analysis dashboard to monitor and display network traffic patterns, bandwidth usage, and application usage.


Version 1.1.0


## Package Contents

- Parser for Cisco ASA Self-Hosted Logs
- Dashboard for Cisco ASA Self-Hosted Logs
    * Cisco-ASA-Overview
    * Cisco-ASA-Events

## Dashboards ( Cisco-ASA-Events)

- Includes  Top  10 various featured messages related to Cisco Networking in Dashboard
- Included  Cisco Severity based on Cisco Classname
	Note: (Cisco utilizes various class related terms in network devices and software)
- Includes Top 10 attempts to access the  destination ports using mnemonic (short abbreviation Cisco code)
- Security Event Analysis: The dashboard displays information about security events and their severity alerts

## Dashboards (Cisco-ASA-Overview)

- Includes ACL access control list that shows top source ip address and top destination ip address used in various aspect of network connectivity
- Include source address with country name and user name with volume
- Include ICMP Connection Warning
- Source ip address activities overtime
- Includes  list of IOC using an to ACL block  based on ip address and ports



## Use Case

- SecOps

## Technology Vendor

Cisco Networking

## Support
Supported by CrowdStrike https://support.crowdstrike.com/

## Installation

1. Install this package in the relevant repository and create a new ingest token for the Cisco Secure Firewall logs parser. Copy this token value. Assign the parser from this package to the token.
2. Configure the firewall to send logs to LogScale.
[Configure Adaptive Security Appliance (ASA) Syslog](https://www.cisco.com/c/en/us/support/docs/security/pix-500-series-security-appliances/63884-config-asa-00.htm)l

More information about the Cisco Secure Firewall ASA Series Syslog Message:[Cisco Syslog Configuration](https://www.cisco.com/c/en/us/td/docs/security/asa/asa917/configuration/general/asa-917-general-config/monitor-syslog.html#ID-2121-0000013b)
[Cisco Syslog Descriptions](https://www.cisco.com/c/en/us/td/docs/security/asa/syslog/b_syslog/b_syslog_index.html)
