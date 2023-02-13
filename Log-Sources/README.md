# Contributing Individual Content and Packages

LogScale Community Content is managed through a Pull Request (PR), Review and Approval process. 

Nobody is able to contribute directly into main. Contributors will need to create a new branch of the LogScale Community Content prior to submitting content and packages via a PR.

+ [Contributing Individual Content](#contributing-individual-content)
+ [Creating Build and Submitting Packages via the Git Commandline](#creating-build-and-submitting-packages-via-the-git-commandline)
+ [Create a New Log Source](#create-a-new-log-source)
+ [Stage, Commit and PR via the Git Commandline](#stage-commit-and-pr-via-the-git-commandline)

If you are struggling with GitHub or the process, reach out via an [Issue](https://github.com/CrowdStrike/logscale-community-content/issues) and we can do it for you. We are here to help.

## Contributing Individual Content

***NOTE:*** We may on a regular basis roll individual content controibutions into an appropriate package

   - Create or export your dashboard, query, or alert. The file name should reflect the purpose, e.g. CVE-2011-0762.yaml.

   - Add descriptive comments at the top of the file. Comments start with // 

      e.g. `// This is my comment.`
      
### Contributing Individual Content via the GitHub Web Site
   - If the Log Source does not exist follow the [Create a New Log Source](#create-a-new-log-source) steps below to create the appropriate folder structure

   - Change to the appropriate ***Content*** sub-folder under the Vendor and Application it is associated with. If required you may need to create the folder. Please refer to the template Application for examples of mandatory content folder names [here](https://github.com/CrowdStrike/logscale-community-content/tree/main/Log-Sources/00_Vendor-Template/Application/Content)

      e.g. `CrowdStrike/FLTR/queries`

   - Create a new file and upload the file to exported from LogScale earlier. You will be prompted to create a new branch to stage the changes in.

   - Repeat for other individual content

   - Submit the pull request.

### Contributing Individual Content via the Git Commandline

   - If the Log Source does not exist follow the [Create a New Log Source](#create-a-new-log-source) steps below to create the appropriate folder structure

  - Change to the appropriate ***Content*** sub-folder under the Vendor and Application it is associated with. If required you may need to create the folder. Please refer to the template Application for examples of mandatory content folder names [here](https://github.com/CrowdStrike/logscale-community-content/tree/main/Log-Sources/00_Vendor-Template/Application/Content)

  - Copy into the approprite directory the file to exported from LogScale earlier
  
  - Repeat for other individual content
  
  - Stage, Commit and create a Pull Request. Refer to [Stage, Commit and PR](#stage-commit-and-pr-via-the-git-commandline) for the required steps

## Creating, Build and Submitting Packages via the Git Commandline
Packages are generally considered to be more "complete" in the sense that they generally includes multiple queries, dashboards, etc. We highly recommend that you contribute/update Packges from the Git commandline via bash or zsh shell with the supplied packaging shell script.

If the Log Source does not exist follow the [Create a New Log Source](#create-a-new-log-source) steps below to create the appropriate folder structure

### Create Package

1. Log into your LogScale instance and open the Repository containing your created content
2. Select Settings | Create a Package | Export Package
3. Provide the following information and click Next
    
    **Note: values in BOLD should not be changed**
  - Scope: **logscale-community-content**
  - Package Name: <vendor_application>
  - Description: This text is used for displaying in lists to give a ~10 word intro.
  - Icon: Use a tool such as https://dataurl.app/ to data URL encode yor package image
  - Version: 0.1.0 
    
    Recommendations on versioning can be found here - https://library.humio.com/falcon-logscale/packages-developer-guidelines-contents.html#packages-developer-guidelines-contents-version
  - Type: **Application**
4. Select your content you would like included in your package
5. Click Export Package and choose a temporary working directory

## Build the Package via the Git Commandline

1. Extract the package zip file in the temporary directory

   `unzip -o community--vendor-application--1.0.0.zip`

2. Replace the README.md with README-template.md

   `mv README-template.md README.md`

3. Review and Update the following files as required
  - manifest.yaml
  - README.md
  
4. Copy the **README.md** and **manifest.yaml** files to the **Packages** directory, under the appropriat Vendor/Application in your local cloned repository

5. Copy the Content directories, queries, dashboards, etc., to the **Content** directory, under the appropriate Vendor/Application in your local cloned repository
   
6. Optionally, build the new package. If you choose not to build the package we will do that for you.

   Change to the **Packages** directory and run the package build script

      `./package-export-build.sh`
    
   Verify the package was created in the Packages directory.  You'll end up with something like this:

      `2023-01-29_21-54-03`
    
   Test the new package

    1. Create a new View and specify the repository from step 3.
    2. Select Settings | Installed | Import Package 
    3. Specify the package zip file created in step 14.
    4. Verify all content has been imprted correctly and operating as expected
   
8. Stage, Commit and create a Pull Request. Refer to [Stage, Commit and PR](#stage-commit-and-pr-via-the-git-commandline) for the required steps

## Create a New Log Source

### Create a New Log Source via the GitHub Web Site

The following blog provides a great walkthrough for creating folder structures in GitHub via the Web Site -
https://medium.com/@kartikagrawal7196/how-to-create-a-folder-in-a-github-repository-36b0fd8f9bf8

### Create a New Log Source via the Git Commandline
1. Clone the repository 

   `git clone https://github.com/CrowdStrike/logscale-community-content.git`
   
2. Change to the ***logscale-community-content*** directory

      `cd logscale-community-content`
   
3. Create a new branch with an appropriate name

   e.g. `git branch <username>-update-XXX-content`
   
4. Switch to the newly created branch

   e.g. `git checkout <username>-update-XXX-content`

5. Copy the template folder for new vendor content and rename it apprpriately
   
   `cp -r 00_Vendor-Template Vendor-Name`
   
6. Rename the new Vendor Application appropriately
   
   `cd Vendor-Name`
   
   `mv Application Application-Name`

## Stage, Commit and PR via the Git Commandline
- Stage Added, Removed and Modified files and directories

   `git add .`
   
- Check to make sure all changes have bee staged

   `git status`
   
- Commit staged files and directories

   `git commit -m "<Commit Comment>"`
 
- Create Pull Request

   `git push --set-upstream origin <branch name>`
   
- Log into the [LogScale Community Content Repository](https://github.com/CrowdStrike/logscale-community-content)

- When prompted create the Pull Request

Once your contribution is merged into main we will delete your branch.
