# CrowdStrike Core FLTR Package

This package contains a robust set of content for use with FLTR. 

# Install

This is meant to be installed in a **view** of the FLTR repo, not the repo itself. 

Prior to installation, please uninstall any related versions of this package that did not originate from the Marketplace, e.g. a version of this package downloaded from the CrowdStrike GitHub site. 

This package will generate an `fdr_aidmaster.csv` mapping file every 3 hours. You may receive a query error about the file not being found prior to the initial generation. To force the generation of this file before the 3 hour window:

1. Go to both *Alerts -> Scheduled Searches -> FLTR aidmaster Generation* scheduled search.
2. Change the *Search schedule* to `* * * * *` and click *Save scheduled search*.
3. Wait approximately 1-2 minutes.
4. Click on *Alerts -> Scheduled Searches*. This should now show a *Last Triggered* time for the *FLTR aidmaster Generation* scheduled search. This means the file has been generated.

**Do not skip these next steps**. 

Revert the settings after the file has been generated:

1. Go back to the *FLTR aidmaster Generation* scheduled search in *Alerts -> Scheduled Searches*.
2. Change the *Search schedule* back to the original value of `H */3 * * *`.
3. Click *Save scheduled search*.

# Changelog

`1.3.2`:

- Initial public release. 

# Package Contents

## Dashboards

There is a selection of dashboards for getting quick value with FLTR. These may serve as the basis for building custom FLTR dashboards, alerts, and queries to match your specific use case.

## Queries

This package provides a wide range of saved queries. These can all be customized or used as a reference point for building additional queries. There is also a selection of user functions to assist with commonly used queries. 

## Event Interactions

Event interactions are included for both `aid` and `UserName` fields. This allows you to quickly pivot between the search and dashboard sections. 

## Schedules Searches

A scheduled search is included that generates the `fdr_aidmaster.csv` lookup file for matching the `aid` to `ComputerName` values. 

# Use Case

- SecOps
