# Crowdstrike FLTR Tutorial

This repository contains a package for using FLTR data feeds.

## Development

Remember to update the change log in `src/README.md` when making changes to the package.

## Deployment Testing

To deploy and test this package:

 1. install the [Humio CLI](https://github.com/humio/cli), or 
 2. clone this repository and run `build.sh` to create a ZIP file. 

The package can be verified by importing it into LogScale from *Settings -> Installed -> Import Package*. 

## Releasing

Please reach out to Kasper Andersen <kasper.andersen@crowdstrike.com> to release a new version.

To prepare a release, please check that:

1. the version string in `src/manifest.yaml` is correct, and
2. the changelog in `src/README.md` is up-to-date
