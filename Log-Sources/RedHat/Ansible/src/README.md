# Analyzing Ansible logs using LogScale

This log package can be used to parse incoming ansible logs via Humio Log Collector.
Logs can be easily ingested into Humio by utilizing parser and Humio Log Collector.
The Parser is capable of parsing logs into fields. The logs will be ingested with the UTC timezone. 


## Package Contents

- Parser for Ansible log (syslog)

- The events are structured using parser to ensure that events timestamp are captured and parsed correctly.
- Sample Dashboards from Ansible logs

- Dashboard helps to monitor event logs with LogScale. It is composed to view server activities in the form of various graphs and tables of relevant data. 

- The package provides quires that will help to identify alerts when the packages was not successfully installed due to various reaon like  server unreachable, busy and other reason.

## Use Case

- SecOps


## Support

This package is supported by our product support team. If you have any issues implementing or running this package, please go to support@crowdstrike.com for assistance.

## Dependencies

- Ansible must be configured to ship logs to a LogScale(Humio) via any compatible log shipper that can wrap logs in JSON.

- Ansible 2.5 and above work with Python 3
Ansible will automatically detect and use Python 3 on many platforms that ship with it.
- Tested  on version Ansible 

## Configuration

- To save Ansible output in a single log on the control node, set the log_path in the configuration path setting. as for example:
/etc/Ansible/ansible.cfg

- Sample of Ansible.cfg 

  [defaults]

  log_path = /var/log/ansible.log


## Installation

## -  Prepare LogScale
- Setup the Ingest Repository
- select, or create a target ingest repository



- Ansible is an open-source community project sponsored by Red Hat
- It can be installed in most of the platform.
-   Installation of the package is straight forward, the installation will deploy the parser, saved queries, and dashboards directly into the repository you install the package into. You will need to install the Humio Log Collector and configure your the config.yaml file in order to ingest system logs.

## How to configure  LogScale (  Humio Log Collector) 
[HumioLogCollector]( https://library.humio.com/humio-server/log-shippers-log-collector-install-linux.html)

- Sample of Humio Log Clollector configuration
   rces:
  var_log:
    type: file
    include: /var/log/ansible.log
    exclude: /var/log/*.gz
    multiLineBeginsWith: ^20\d{2}-
    sink: humio
sinks:
  humio:
    type: humio
    token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    url: https://cloud.community.humio.com/
    encodingCodec: json

## Document

[Documentation](https://docs.google.com/document/d/1BaozU09pIAAIas9ubdtxdDXoyn3b6jCs3NEY6kiQMKc/edit#heading=h.llu2egq1xfnb)
