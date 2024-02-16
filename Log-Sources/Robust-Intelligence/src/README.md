# Robust Intelligence AI Firewall LogScale Package

## Overview

The [Robust Intelligence AI Firewall][1] is a real-time protective layer for AI models.

The AI Firewall inspects incoming user prompts to flag malicious or harmful payloads, including any that attempt prompt injection, prompt extraction, or personally identifiable information(PII) extraction. The AI Firewall also scans LLM model output to ensure it's free of false information, sensitive data, and harmful content. Responses that fall outside your organization's standards can then be blocked from the application.

This integration monitors the AI Firewall results using LogScale. It provides users with observability of their AI security issues including metrics for allowed data points, flagged data points, and insight on why each data point was flagged.

## Setup

Follow the instructions below to enable AI Firewall's log forwarding to Crowdstrike LogScale server:

1. Install this package to your LogScale repository and create a new ingest token for Robust_Intelligence_Firewall_Parser parser. 
2. Enable log forwarding to LogScale in the rime-extras terraform package. Set the following variables on the rime-extras terraform module to enable log forwarding to LogScale:
     - install_logscale_fluentbit = true
     - logscale_hostname = <logscale_hostname>
     - logscale_ingest_token = <logscale_ingest_token>
   
     If your AI firewall instance is managed by Robust Intelligence, please contact [Robust Intelligence Support][2] to enable Firewall validation logs forwarding to the LogScale instance.
## Troubleshooting

Need Help? Contact [Robust Intelligence Support][2].

[1]: https://www.robustintelligence.com/platform/ai-firewall
[2]: mailto:help@robustintelligence.com
