# CrowdStrike FLTR Run Package

This package includes enrichment functions and lookups that can be leveraged by FLTR packages. 

# Install

The `crowdstrike/fltr-run` package is meant to be installed in a **view** of the FLTR repo, not the repo itself. 

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

`1.3.0`: 

- Initial public release. 

# Package Contents

## Queries

The included queries are designed to act as user functions for commonly used queries. These are used extensively in the `crowdstrike/fltr-core` package. 

## Scheduled Searches

A scheduled search is included that generates the `aid` to `ComputerName` mapping. 

## Actions

An action is included that saves the lookup file referenced above. 

# Use Case

- SecOps
