# :warning: Warning :warning:

This package is **unofficial** and is not a replacement for the [LogScale Package Marketplace](https://library.humio.com/humio-server/packages-marketplace.html). It is primarily used by the CrowdStrike SE team as learning examples. 

# Description

This package includes enrichment functions and lookups that can be leveraged by Falcon data content packages. It should be installed in the Falcon data **view** prior to installing any Falcon data content packages. 

# Install
- Create a view of your Falcon data repository.
- Install the package by going to Settings -> Installed -> Import Package within the created view.

# Install Notes
A scheduled query is installed that will generate an `falcondata_aidmaster.csv` file every 3 hours. You will receive a query error about the file not being found prior to the initial generation. To force the generation of this file before the 3 hour window:

- Go to *Alerts -> Scheduled Searches -> Falcon Data aidmaster Scheduled Search*.
- Change the *Search schedule* to `* * * * *` and click *Save scheduled search*.
- Wait approximately 1-2 minutes.
- Click on *Alerts -> Scheduled Searches*. This should now show a *Last Triggered* time for *Falcon Data aidmaster Scheduled Search*. This means the file has been generated.

**Do not skip these next steps**. Revert the settings after the file has been generated:

- Go back to the *Falcon Data aidmaster Scheduled Search* in *Alerts -> Scheduled Searches*.
- Change the *Search schedule* back to the original value of `H */3 * * *`.
- Click *Save scheduled search*.
