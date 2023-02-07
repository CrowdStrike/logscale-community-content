# CrowdStrike FLTR Run Package

This package includes enrichment functions and lookups that can be leveraged by FLTR packages. 

# Install

This is meant to be installed in a **view** of the FLTR data, *not* the repo. 

Two scheduled queries are installed that will generate `fltr_aidmaster.csv` files every 3 hours. You will receive a query error about the file not being found prior to the initial generation. To force the generation of this file before the 3 hour window:

- Go to both *Alerts -> Scheduled Searches -> FLTR aidmaster* scheduled searches.
- Change the *Search schedule* to `* * * * *` and click *Save scheduled search*.
- Wait approximately 1-2 minutes.
- Click on *Alerts -> Scheduled Searches*. This should now show a *Last Triggered* time for *Falcon Data aidmaster Scheduled Search*. This means the file has been generated.

**Do not skip these next steps**. Revert the settings after the file has been generated:

- Go back to both *FLTR aidmaster* scheduled searches in *Alerts -> Scheduled Searches*.
- Change the *Search schedule* back to the original value of `H */3 * * *`.
- Click *Save scheduled search*.

# Changelog

- 1.2.0 
  - Initial public release. 

# Package Contents

## Queries

The included queries are designed to act as user functions for commonly used queries. 

## Scheduled Searches

A scheduled search is included that generates the `aid` to `ComputerName` mapping. 

## Actions

An action is included that saves the lookup file referenced above. 

# Use Case

- SecOps
