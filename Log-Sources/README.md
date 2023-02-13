# Contributing Individual Content and Packages

❗LogScale Community Content is managed through a Pull Request (PR), Review and Approval process. Nobody is able to contribute directly into main. Contributors will need to create a new branch of the LogScale Community Content before prior to submitting content and packages via a PR.❗

+ [Contributing Individual Content](#contributing-individual-content)
+ [Creating and Submitting Packages](#creating-and-submitting-packages)
+ [Create a New Log Source](#create-a-new-log-source)

## Contributing Individual Content

   - Create or export your dashboard, query, or alert. The file name should reflect the purpose, e.g. CVE-2011-0762.yaml.

   - Add descriptive comments at the top of the file. Comments start with // 

      e.g. `// This is my comment.`
      
### Contributing via the GitHub Web Site



   - Save the file into the ***Content*** directory within the appropriate Log Source directory, e.g. CrowdStrike/FLTR/queries.

### Contributing via Git commandline

- Submit the pull request.

## Creating and Submitting Packages
Packages are generally considered to be more "complete" in the sense that they generally includes multiple queries, dashboards, etc. The process of creating a package is fairly simple. You'll want to do this from a bash or zsh shell.

- Go into the top-level Packages directory of the forked repo. Create a directory reflecting the name and product of the package you're creating. The first directory is the generally the company name, and the subdirectory is generally the product name, e.g. MyVendor/MyPackage. Just create a new package directory in the vendor directory if the vendor directory already exists.

- Start by exporting the package from LogScale or FLTR. This should generally be exported as an Application. Use whatever you'd like for the mandatory fields since we'll replace them later.

- Save the exported package to the subdirectory you'd created above, e.g. MyVendor/MyPackage.

- Uncompress the package and delete the zip file, e.g. unzip MyVendor--MyPackage--0.1.0.zip; rm -f MyVendor--MyPackage--0.1.0.zip.

- Delete the files README.md and manifest.yaml that were just created, i.e. rm -f README.md manifest.yaml. You'll add new ones in the next step.

- Save the files README.md, manifest.yaml, and package-export-build.sh in the subdirectory you'd created, e.g. the MyPackage directory of MyVendor/MyPackage. Right-click and "Save As" is the easiest method.

- Modify the README.md and manifest.yaml files as needed. Please be sure to use a code editor, e.g. vim, Visual Studio Code, etc. Office suite applications will likely break the text formatting.

- Run the command bash ./package-export-build.sh from the CLI. This will build the package. You'll end up with something like this:

   `2023-01-29_21-54-03`

- All done! Submit the pull request.


## Create a New Log Source

### Via the GitHub Web Site

### Via Git commandline
1. Clone the repository 

   `git clone https://github.com/CrowdStrike/logscale-community-content.git`

2. Copy the template folder for new vendor content and rename it apprpriately

   `cd logscale-community-content`
   
   `cp -r 00_Vendor-Template Vendor-Name`
   
3. Rename the new Vendor Application appropriately
   
   `cd Vendor-Name`
   
   `mv Application Application-Name`

## Create Package
1. Log into your LogScale instance and open the Repository containing your created content
2. Select Settings | Create a Package | Export Package
3. Provide the following information and click Next
    
    **Note: values in BOLD should not be changed**
  - Scope: **logscale-community-content**
  - Package Name: <vendor_application>
  - Description: This text is used for displaying in lists to give a ~10 word intro.
  - Icon: Use a tool such as https://dataurl.app/ to data URL encode yor package image
  - Version: 1.0.0 
    
    Recommendations on versioning can be found here - https://library.humio.com/falcon-logscale/packages-developer-guidelines-contents.html#packages-developer-guidelines-contents-version
  - Type: **Application**
4. Select your content you would like included in your package
5. Click Export Package and choose the "src" subdirectory under the new directory you created in step 2

## Submit Package via the GitHub Web Site

## Submit Package via Git commandline

1. Extract the package zip file

   `unzip -o community--vendor-application--1.0.0.zip`

2. Replace the README.md with README-template.md

   `mv README-template.md README.md`

3. Review and Update the following files as required
  - manifest.yaml
  - README.md
  
4. Delete the original package

    `rm -f community--vendor-application--1.0.0.zip`
   
5. Optionally, update the ARCHIVE value in build.sh with the new package name and build the package

    `cd ../`
    
    `vi build.sh`. <- ARCHIVE=vendor--app--${VERSION}.zip
   
    `./build.sh`
    
6. Verify the package was created in the Packages directory
    
7. Test the new package

    1. Create a new View and specify the repository from step 3.
    2. Select Settings | Installed | Import Package 
    3. Specify the package zip file created in step 14.
    4. Verify all content has been imprted correctly and operating as expected
   
8. Stage, Commit and create a Pull. Refer to [INSERT LINK TO GITHUB STEPS] for an overview of working with Git
