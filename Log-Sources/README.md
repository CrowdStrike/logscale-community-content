# Create a new Log Source
## Via the GitHub Web Site

## Via Git commandline
1. Clone the repository 

   `git clone https://github.com/CrowdStrike/logscale-community-content.git`

2. Copy the template folder for new vendor content and rename it apprpriately

   `cd logscale-community-content`
   
   `cp -r 00_Vendor-Template Vendor-Name`
   
3. Rename the new Vendor Application appropriately
   
   `cd Vendor-Name`
   
   `mv Application Application-Name`

# Add a new Package
## Via the GitHub Web Site

## Via Git commandline
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
6. Extract the package zip file

   `unzip -o community--vendor-application--1.0.0.zip`

7. Replace the README.md with README-template.md

   `mv README-template.md README.md`

8. Review and Update the following files as required
  - manifest.yaml
  - README.md
  
9. Delete the original package

    `rm -f community--vendor-application--1.0.0.zip`
   
10. Optionally, update the ARCHIVE value in build.sh with the new package name and build the package

    `cd ../`
    
    `vi build.sh`. <- ARCHIVE=vendor--app--${VERSION}.zip
   
    `./build.sh`
    
11. Verify the package was created in the Packages directory
    
12. Test the new package

    1. Create a new View and specify the repository from step 3.
    2. Select Settings | Installed | Import Package 
    3. Specify the package zip file created in step 14.
    4. Verify all content has been imprted correctly and operating as expected
   
13. Stage, Commit and create a Pull. Refer to [INSERT LINK TO GITHUB STEPS] for an overview of working with Git
