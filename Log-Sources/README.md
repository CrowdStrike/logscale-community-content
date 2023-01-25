# Create a new Log Source
1. Ensure you have a most recent copy of the repository. Refer to [INSERT LINK TO GITHUB STEPS] for an overview of working with Git
2. Copy the template folder for new vendor content and rename appropiately and in alignment with naming standards
3. Log into your LogScale instance and open the Repository containing your created content
4. Select Settings | Create a Package | Export Package
5. Provide the following information and click Next
    
    **Note: values in BOLD should not be changed**
  - Scope: **community**
  - Package Name: <vendor_application>
  - Description: This text is used for displaying in lists to give a ~10 word intro.
  - Icon: Use a tool such as https://dataurl.app/ to data URL encode yor package image
  - Version: 1.0.0 
    
    Recommendations on versioning can be found here - https://library.humio.com/falcon-logscale/packages-developer-guidelines-contents.html#packages-developer-guidelines-contents-version
  - Type: **Application**
6. Select your content you would like included in your package
7. Click Export Package and choose the "src" subdirectory under the new directory you created in step 2
8. Extract the package zip file

   `unzip -o community--vendor-application--1.0.0.zip`

9. Replace the README.md with README-template.md

   `mv README-template.md README.md`

10. Review and Update the following files as required
  - manifest.yaml
  - README.md
  
11. Delete the original package

    `rm -f community--vendor-application--1.0.0.zip`
   
12. Optionally, update the ARCHIVE value in build.sh with the new package name and build the package

    `cd ../`
    
    `vi build.sh`. <- ARCHIVE=vendor--app--${VERSION}.zip
   
    `./build.sh`
    
13. Verify the package was created in the Packages directory
    
14. Test the new package

    1. Create a new View and specify the repository from step 3.
    2. Select Settings | Installed | Import Package 
    3. Specify the package zip file created in step 14.
    4. Verify all content has been imprted correctly and operating as expected
   
15. Stage, Commit and create a Pull. Refer to [INSERT LINK TO GITHUB STEPS] for an overview of working with Git
