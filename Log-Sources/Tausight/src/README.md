# **Tausight/ePHI-Risk-Posture**
Electronic Protected Health Information (ePHI) is at the core of modern digital health and as such, has incredible value for the cyber criminal using it for ransom, extortion or exploitation. 
Integrating Tausight’s ePHI intelligence gathered from sensors on endpoint devices, scanners for NAS, cloud and email servers in CrowdStrike Falcon® LogScale, allows cybersecurity and privacy teams to proactively mitigate cyber risks. This package contains dashboards, scheduled searches, saved queries, and alerts designed for Tausight sensor data to highlight the ePHI breach risk in a healthcare environment. You can learn more about the [Tausight ePHI Risk Posture here](https://www.tausight.com/). 

## Package Contents

The following components will be loaded into your LogScale repo when you install the Tausight package from the Crowdstrike Marketplace

- **Parser**
  - *tausight-json*

- **Dashboards**
  - *Tausight: Alerts*
Realtime ePHI intelligence allowing the IT team to visualize and act on risks to ePHI across the healthcare organization

  - *Tausight: ePHI Inventory*
ePHI at-rest for assessing where and how ePHI is stored across the healthcare organization

  - *Tausight: ePHI Ownership*
ePHI usage awareness allowing organizations to reduce risk and exposure by ensuring appropriate access controls and retention policies are adhered to 

  - *Tausight: ePHI Activity*
ePHI movement risk measures provide insight to user/application interactions that might result in compromise or loss of ePHI

  - *Tausight: eMail Activity*
ePHI eMail risk awareness highlighting the potential exposures from ePHI leaving the organization 

  - *Tausight: ePHI Details* and *Tausight: ePHI Activity Details*
ePHI storage and movement details allowing the IT and compliance teams to understand and reduce the magnitude of impacted lives from a potential ransom, breach, device loss, or other ePHI threats

- **Scheduled Search**
  - Generate Endpoint Information

- **Queries**
  - Tausight\_AttachmentHasEphi
  - Tausight\_EmailHasEphi
  - Tausight\_ePHIMovement
  - Tausight\_ePHIMovementWithJoins
  - Tausight\_ePHIStored
  - Tausight\_ePHIStoredWithJoins

- **Alerts** (with no action defined)
  - Compliance violations: ePHI moved to unauthorized removable media
  - Compliance violations: Unencrypted laptop device with ePHI
  - Suspicious activity: ePHI moved/copied to unencrypted removable media
  - Vulnerabilities: creator/owner with excessive number of ePHI files
  - Vulnerabilities: creator/owner with excessive number of stale/unused ePHI files
  - Vulnerabilities: Unencrypted laptop detected


## Use Case
- SecOps
- ITOps


## Technology Vendor
Tausight Inc. [https://www.linkedin.com/company/tausight/](https://www.linkedin.com/company/tausight/about/)


## Support
This package is supported by Tausight Inc. <https://www.tausight.com/>, [https://www.linkedin.com/company/tausight/](https://www.linkedin.com/company/tausight/about/), support@tausight.com

## Dependencies
N/A

## Installation
The installation will automatically deploy the ‘tausight-json’ parser, dashboards, alerts, scheduled search and saved queries directly into the destination repository. The ingest needs to be configured by an ingest token using the ‘tausight-json’ parser that comes with the package.

To obtain sample Tausight sensor data please refer to the [CrowdStrike Logscale Community Github repository](https://github.com/CrowdStrike/logscale-community-content) or contact us at <support@tausight.com>.

To ingest live data from your own endpoints, please contact Tausight <support@tausight.com>.


