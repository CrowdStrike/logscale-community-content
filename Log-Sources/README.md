# Contributing Individual Content and Packages

LogScale Community Content is managed through pull requests. 

Contributors will need to create a new branch of the LogScale Community Content prior to submitting content and packages via a PR.

- [Contributing Individual Content and Packages](#contributing-individual-content-and-packages)
  - [Contributing Individual Content](#contributing-individual-content)
    - [Contributing Individual Content via the GitHub Web Site](#contributing-individual-content-via-the-github-web-site)
    - [Contributing Individual Content via the Git Commandline](#contributing-individual-content-via-the-git-commandline)
  - [Creating, Building, and Submitting Packages via the Git Commandline](#creating-building-and-submitting-packages-via-the-git-commandline)
    - [Creating a Package](#creating-a-package)
  - [Building the Package via the Git Commandline](#building-the-package-via-the-git-commandline)
  - [Creating a New Log Source](#creating-a-new-log-source)
    - [Creating a New Log Source via the GitHub Web Site](#creating-a-new-log-source-via-the-github-web-site)
    - [Creating a New Log Source via the Git Commandline](#creating-a-new-log-source-via-the-git-commandline)
  - [Staging, Committing, and PR via the Git Commandline](#staging-committing-and-pr-via-the-git-commandline)

If you are struggling with GitHub or the process, reach out via an [Issue](https://github.com/CrowdStrike/logscale-community-content/issues) and we can do it for you. We are here to help.

## Contributing Individual Content
Individual content is "ad-hoc" content such as Queries, Dashboards, Parsers, etc. without a full package.

***NOTE:*** We may on a regular basis roll individual content contributions into an appropriate package

   1. Create or export your dashboard, query, or alert. The file name should reflect the purpose, e.g. CVE-2011-0762.yaml.

   2. Add descriptive comments at the top of the file. Comments start with // 

      e.g. `// This is my comment.`
      
### Contributing Individual Content via the GitHub Web Site
   1. If the Log Source does not exist follow the [Create a New Log Source](#create-a-new-log-source) steps below to create the appropriate folder structure

   2. Change to the appropriate ***Content*** sub-folder under the Vendor and Application it is associated with. If required you may need to create the folder. Please refer to the template Application for examples of mandatory content folder names [here](https://github.com/CrowdStrike/logscale-community-content/tree/main/Log-Sources/00_Vendor-Template/Application/Content)

      e.g. `CrowdStrike/FLTR/queries`

   3. Create a new file and upload the file to exported from LogScale earlier. You will be prompted to create a new branch to stage the changes in. Please use a branch name similar to this:

   `<username>-update-XXX-content`

   4. Repeat for other individual content

   5. Submit the pull request.

### Contributing Individual Content via the Git Commandline

   1. If the Log Source does not exist follow the [Create a New Log Source](#create-a-new-log-source) steps below to create the appropriate folder structure

  2. Change to the appropriate ***Content*** sub-folder under the Vendor and Application it is associated with. If required you may need to create the folder. Please refer to the template Application for examples of mandatory content folder names [here](https://github.com/CrowdStrike/logscale-community-content/tree/main/Log-Sources/00_Vendor-Template/Application/Content)

  3. Copy into the appropriate directory the files to exported from LogScale earlier
  
  4. Repeat for other individual content
  
  5. Stage, Commit and create a Pull Request. Refer to [Stage, Commit and PR](#stage-commit-and-pr-via-the-git-commandline) for the required steps

## Creating, Building, and Submitting Packages via the Git Commandline
Packages are generally considered to be more "complete" in the sense that they generally includes multiple queries, dashboards, etc. We highly recommend that you contribute/update Packges from the Git commandline via bash or zsh shell with the supplied packaging shell script.

If the Log Source does not exist follow the [Create a New Log Source](#create-a-new-log-source) steps below to create the appropriate folder structure

### Creating a Package

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

## Building the Package via the Git Commandline

1. Extract the package zip file in the temporary directory

   `unzip -o community--vendor-application--1.0.0.zip`

2. Replace the README.md with README-template.md in the top level directory

   `mv README-template.md README.md`

3. Review and Update the following files as required
  - manifest.yaml
  - README.md
  
4. Copy the **README.md** file to the **top level** directory, under the appropriate Vendor/Application in your local cloned repository

5. Copy the **manifest.yaml** file to the **Packages** directory, under the appropriate Vendor/Application in your local cloned repository

5. Copy the Content directories, queries, dashboards, etc., to the **Content** directory, under the appropriate Vendor/Application in your local cloned repository
   
6. Optionally, build the new package. If you choose not to build the package we will do that for you.

   Change to the **Packages** directory and run the package build script

      `./package-export-build.sh`
    
   Verify the package was created in the Packages directory.  You'll end up with something like this:

      `2023-01-29_21-54-03`
    
   Test the new package

    1. Create a new View and specify the repository from where you exported the package earlier. **NOTE**: You will need to test in a Repository directly if your package contains one or more parsers
    2. Select Settings | Installed | Import Package 
    3. Specify the package zip file created in step 6.
    4. Verify all content has been imprted correctly and operating as expected
   
7. Stage, Commit and create a Pull Request. Refer to [Stage, Commit and PR](#stage-commit-and-pr-via-the-git-commandline) for the required steps

## Creating a New Log Source

### Creating a New Log Source via the GitHub Web Site

The following blog provides a great walkthrough for creating folder structures in GitHub via the Web Site -
https://medium.com/@kartikagrawal7196/how-to-create-a-folder-in-a-github-repository-36b0fd8f9bf8

### Creating a New Log Source via the Git Commandline
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

## Staging, Committing, and PR via the Git Commandline

1. Make sure you are at the top level directory - ***logscale-community-content***

2. ***MAC USERS ONLY*** remove all .DS_STORE files

   `find . -name '.DS_Store' -type f -delete`

3. Stage Added, Removed and Modified files and directories

   `git add .`
   
4. Check to make sure all changes have bee staged

   `git status`
   
5. Commit staged files and directories

   `git commit -m "<Commit Comment>"`
 
6. Create Pull Request

   `git push --set-upstream origin <branch name>`
   
7. Log into the [LogScale Community Content Repository](https://github.com/CrowdStrike/logscale-community-content)

8. When prompted create the Pull Request

Once your contribution is merged into main we will delete your branch.
