# Contributing Config Samples

LogScale Community Content is managed through a Pull Request (PR), Review and Approval process. 

Nobody is able to contribute directly into main. Contributors will need to create a new branch of the LogScale Community Content prior to submitting content and packages via a PR.

+ [Contributing Config Samples](#contributing-config-samples)
+ [Create a New Config Sample](#create-a-new-config-sample)
+ [Stage, Commit and PR via the Git Commandline](#stage-commit-and-pr-via-the-git-commandline)

If you are struggling with GitHub or the process, reach out via an [Issue](https://github.com/CrowdStrike/logscale-community-content/issues) and we can do it for you. We are here to help.

## Contributing Config Samples

   - Create or export your Config Sample. The file name should reflect the purpose, e.g. windows_event_codes.csv

   - Add descriptive comments at the top of the file. Comments start with // 

      e.g. `// This is my comment.`
      
### Contributing Config Samples via the GitHub Web Site
   - If an appropriate Config Sample directory does not exist follow the [Create a new Config Samples Directory](#create-a-new-config-samples-directory) steps below to create the appropriate folder structure

      e.g. `Config-Samples/Log-Shippers/Fluentd`

   - Create a new file and upload the Config Sample. You will be prompted to create a new branch to stage the changes in.

   - Repeat for other Config Samples

   - Submit the pull request.

### Contributing Config Samples via the Git Commandline

  - If an appropriate Config Samples directory does not exist follow the [Create a new Config Samples Directory](#create-a-new-config-samples-directory) steps below to create the appropriate folder structure

      e.g. `Config-Samples/Log-Shippers/Fluentd`
      
  - Copy into the approprite directory your Config Sample
  
  - Repeat for other Config Samples
  
  - Stage, Commit and create a Pull Request. Refer to [Stage, Commit and PR](#stage-commit-and-pr-via-the-git-commandline) for the required steps

## Create a New Config Sample

### Create a New Config Sample via the GitHub Web Site

The following blog provides a great walkthrough for creating folder structures in GitHub via the Web Site -
https://medium.com/@kartikagrawal7196/how-to-create-a-folder-in-a-github-repository-36b0fd8f9bf8

### Create a New Config Sample via the Git Commandline
1. Clone the repository 

   `git clone https://github.com/CrowdStrike/logscale-community-content.git`
   
2. Change to the ***logscale-community-content*** directory

      `cd logscale-community-content`
   
3. Create a new branch with an appropriate name

   e.g. `git branch <username>-update-XXX-config-sample`

4. Create a new folder under the Config-Sample directory
   
   `mkdir Config-Sample\new_Config-Sample`

## Stage, Commit and PR via the Git Commandline
- Stage Added, Removed and Modified files and directories

   `git add .`
   
- Commit staged files and directories

   `git commit -m "<Commit Comment>`
 
- Create Pull Request

   `git push`

Once your contribution is merged into main we will delete your branch.
