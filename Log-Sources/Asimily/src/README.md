# README
## Asimily IoMT

Dashboard and parser for enabling organizations to run advanced device and risk analyses for all devices including unmanaged (IoT/IoMT/OT).

www.asimily.com

## Package Contents
- Parser for Asimily anomaly data
- Alert Dashboard

## Use Case
- IoT
- IoMT

## Technology Vendor
Asimily

## Support
Supported by LogScale and Asimily. https://support.humio.com/ and support@asimily.com

## Dependencies
> The parser included assumes data is sent from Asimily in JSON format.

# Asimily LogScale Configuration
​
## Setup
​
1. In your LogScale Settings page, navigate to **Ingest tokens** under **Ingest**.
2. Click **Add token** and name the token something memorable.
3. Click **Create token**, then view and copy the token you just created.
4. Go to **Configuration**->**Connectors** inside the Asimily Console.
5. Enter the URL you use to log in under **URL** and paste the token you just copied into the **API Token** field.
6. Events should begin sending to LogScale shortly.

Installing the package will automatically deploy the `Asimily`
parser, saved searches, and alerts directly into the repository you
install the package into.
      