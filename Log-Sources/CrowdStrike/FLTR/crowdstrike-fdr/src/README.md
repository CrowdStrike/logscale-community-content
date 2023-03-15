# CrowdStrike FLTR Parser

This package provides a parser for FLTR.

# Breaking Changes

- This will uninstall the previous `crowdstrike/fdr` package contents except for the parser. 
- This will not impact queries or dashboards that have been saved locally.
- If you've made modifications to the `crowdstrike/fdr` package contents and wish to keep them, they can be exported by going to `Settings -> Create a Package -> Export Package`.
- The content portion of this package has been moved to the `crowdstrike/fltr-core` package in the LogScale Marketplace. Please install that for FLTR queries, dashboards, event interactions, etc. 

# Install

This package is meant to be installed in the repo for FLTR. It works for both FDR and Data Connector. Additional packages just as `crowdstrike/fltr-core` should be installed in a view linked to that repo. 

# Changelog

`1.3.2`:

- Initial public release. 

# Package Contents

## Parsers

This includes a parser for FLTR.

# Use Case

- SecOps
