# Contributing Standalone Content
Standalone content is "ad-hoc" content such as queries, dashboards, parsers, etc. This is generally just an export of the YAML file from the LogScale UI. Text files are also fine if it's just copy and paste. Examples can be found here:

https://github.com/CrowdStrike/logscale-community-content/tree/main/Queries-Only

1. Create or export your dashboard, query, or alert. The file name should reflect the purpose, e.g. CVE-2011-0762.yaml.
2. Add descriptive comments at the top of the file. Comments start with `//`. For example: `// This is my comment.`
3. Submit the content as a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

# Creating, Building, and Submitting Packages
Packages are generally considered to be more "complete" in the sense that they generally includes multiple queries, dashboards, etc. Packages can be imported directly in the LogScale UI.

## Requirements for Packages
1. Parser must contain anonymized log samples for validation. These can be added during parser creation in the LogScale UI. Additional examples can be added directly to the YAML file after the package has been exported. 
2. The README should include the method used for log ingestion, e.g. syslog ingested via Falcon LogScale Collector, HEC output from the log source to the LogScale endpoint, flat file being ingested via Falcon LogScale Collector, etc. These instructions should be repeatable by the user. 
3. The `manifest.yaml` file should be updated to include the official logo. 
4. Prioritized fields should be parsed out and normalized into key value pairs.
5. The parser should follow the [Falcon LogScale Package Standards](https://github.com/CrowdStrike/logscale-community-content/wiki/Falcon-Logscale-Package-Standards). 

## Creating a Package Template From the UI
1. Log into your LogScale instance and open the Repository containing your created content.
2. Select `Settings` -> `Create a Package` -> `Export Package`.
3. Provide the following information and click `Next`:
  ```
  Scope: <vendor_name>
  Package Name: <vendor_application>
  Description: This text is used for displaying in lists to give a ~10 word intro.
  Icon: Use a tool such as https://dataurl.app/ to data URL encode yor package image.
  Version: 0.1.0 
  ``` 
4. Type: **Application**
5. Select your content you would like included in your package.
6. Click Export Package and choose a temporary working directory.

## Refining the Package From the Commandline 
1. Extract the package zip file in the temporary directory: `unzip -o vendor--application--1.0.0.zip`
2. Review and update `src/manifest.yaml` and `src/README.md`. You can refer to the [Template Package](00-Vendor-Template) for additional details, e.g. adding lookup files to the package. [Documentation on package creation](https://library.humio.com/integrations/packages-file-formats.html) can be found on the LogScale documentation site. 
3. Export or copy the LogScale YAML files into the appropriate directories under the `src` directory.
4. Copy the [build.sh](00-Vendor-Template/build.sh) file into the directory above `src`. Run the build script: `./build.sh`. The package will be created in the same directory as the `build.sh` script.
5. To test the package, create a new view or repo, and specify the repository from where you exported the package earlier. 
6. Select `Settings -> Installed -> Import Package`.
7. Specify the package zip file created in step 6.
8. Verify all content has been imported correctly and operating as expected.
9. Create and submit a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)