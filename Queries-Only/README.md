![CrowdStrike](https://www.crowdstrike.com/wp-content/uploads/2022/09/CS_Logo_2022_In-Line_All-Red_RGB.png)

# LogScale and FLTR Queries

These are standalone queries for LogScale and FLTR, often situational to CVEs and ATT&CK techniques. Many of them are posted in the [CrowdStrike subreddit](https://www.reddit.com/r/crowdstrike/), including [Cool Query Friday](https://www.reddit.com/r/crowdstrike/?f=flair_name%3A%22CQF%22). The queries can be found above this in the [Queries](Queries) directory.

# Submitting Queries

Have a useful query you'd like to submit? Not a problem! Just submit a [pull request](https://github.com/CrowdStrike/logscale-community-content/pulls) with the query. The filename should follow this format:

`[CVE, ATT&CK ID, or related] Brief description.logscale`

For example:

`[T1552.001] Microsoft Teams Unsecured Credentials In Files.logscale`

`[CVE-2023-36884] Office and Windows HTML Remote Code Execution Vulnerability.logscale`

The file itself should contain a formatted version of the query. You should also include a `// comment` at the top of the query that provides the following:

- The file name so it's easily referenced when looking at the query.
- Links to any relevant information regarding the query. 
- A description of the query.

For example:

```
// [CVE-2023-36884] Office and Windows HTML Remote Code Execution Vulnerability
//
// https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-36884
// https://www.reddit.com/r/crowdstrike/comments/14y1yei/20230712_situational_awareness_microsoft_office/
//
// Identify Word documents being written to disk with a .url extension.

event_platform=Win #event_simpleName=/^(MSDocxFileWritten)$/ TargetFileName=/\.url$/ 
| TargetFileName=/\\.+\\(?<FileName>.+\..+)/i 
| select([@timestamp, aid, FileName, TargetFileName]) 
```

Happy hunting!