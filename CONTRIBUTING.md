# Contributing to this repository <!-- omit in toc -->


_Welcome!_ We're excited you want to contribute to the LogScale Community Content.

Please review this document for details regarding getting started with your first contribution, file formats, standards, and our pull request process. If you have any questions, please let us know by
posting your question in the [Issues](https://github.com/CrowdStrike/logscale-community-content/issues).

**Before you begin**: Have you read the [Code of Conduct](https://github.com/CrowdStrike/logscale-community-content/blob/main/CODE_OF_CONDUCT.md)?

The Code of Conduct helps us establish community norms and how they'll be enforced.

- [How you can contribute](#how-you-can-contribute)
  - [Bug reporting is handled using GitHub issues](#bug-reporting-is-handled-using-github-issues)
  - [All contributions will be submitted under the Unlicense license](#all-contributions-will-be-submitted-under-the-unlicense-license)
  - [Branch targeting](#branch-targeting)
  - [Pull Request restrictions](#pull-request-restrictions)
  - [Approval and Merging](#approval-and-merging)
- [Suggestions](#suggestions)

## How you can contribute
- See something? Say something! Submit a [bug report](https://github.com/CrowdStrike/logscale-community-content/issues) to let the community know what you've experienced or found. Bonus points if you suggest possible fixes or what you feel may resolve the issue. 
- Contribute Content. Either [Content and Packages](https://github.com/CrowdStrike/logscale-community-content/tree/main/Log-Sources) or [Config Samples](https://github.com/CrowdStrike/logscale-community-content/tree/main/Config-Samples).

### Bug reporting is handled using GitHub issues
We use [GitHub issues](https://github.com/CrowdStrike/logscale-community-content/issues) to track:

+ [bugs](https://github.com/CrowdStrike/logscale-community-content/issues?q=is%3Aissue+label%3A%22bug+%3Abug%3A%22) (`BUG`)
+ [documentation](https://github.com/CrowdStrike/logscale-community-content/issues?q=is%3Aissue+label%3A%22documentation+%3Abook%3A%22) and [linking](https://github.com/CrowdStrike/falconpy/issues?q=is%3Aissue+label%3A%22broken+link+%3Alink%3A%22) issues (`DOC`, `LINK`)
+ [enhancements](https://github.com/CrowdStrike/logscale-community-content/issues?q=is%3Aissue+label%3A%22enhancement+%3Astar2%3A%22) (`ENH`)
+ [security concerns](https://github.com/CrowdStrike/logscale-community-content/issues?q=is%3Aissue+label%3Asecurity) (`SEC`)

[Report Issues](https://github.com/CrowdStrike/logscale-community-content/issues/new)

---

### All contributions will be submitted under the Unlicense license
When you submit code changes, your submissions are understood to be under the same Unlicense [license](LICENSE) that covers the repository. If this is a concern, contact the maintainers before contributing.

### Branch targeting
Please do not target the `main` branch with your pull request. 

All pull requests should target a new unique branch using a naming standard that is appropriate.  

Depending on the nature of your pull request, you may be contacted by a maintainer and asked to target a new branch specific to your submission.

### Pull Request restrictions
Please review this list and confirm none of the following concerns exist within your request. Pull requests containing any of these elements will be prevented from merging to the code base and may be closed.

| Concern | Restriction |
| :--- | :--- |
| **Scripts** | Limited exceptions to be reviewed by maintainers on a case by case basis. |
| **Binaries** | Compiled binaries, regardless of intent should not be included in the code base or in samples. |
| **Disparaging references to 3rd party vendors in source or content** | We are here to collaborate regarding LogScale Community Content, not bash the work of others. |
| **Inappropriate language, comments or references found within source or content** | Comments (and comment art) must not detract from code legibility or impact overall package size. **All** content published to this repository (source or otherwise) must follow the [Code of Conduct](https://github.com/CrowdStrike/falconpy/blob/main/CODE_OF_CONDUCT.md). |
| **Intellectual property that is not yours** | Copywrited works, trademarks, source code or image assets belonging to others should not be posted to this repository whatsoever. CrowdStrike assets which are already released into the Public Domain will be accepted as long as their usage meets other restrictions, the rules specified in the [Code of Conduct](https://github.com/CrowdStrike/logscale-community-content/blob/main/CODE_OF_CONDUCT.md), and the guidelines set forth in the [CrowdStrike Brand Guide](https://crowdstrikebrand.com/brand-guide/). |
| **Relative links in README files** | This impacts our package deployment as these files are consumed as part of the build process. All link and image references within README files must contain the full URL. |

### Approval and Merging
All Pull Requests must be approved by at least one maintainer. Once approved, a maintainer will perform the merge and if required execute any backend processes related to packaging. 

At this point in time, `main` is a protected branch.

## Suggestions
If you have suggestions on how this process could be improved, please let us know by raising an [issue](https://github.com/CrowdStrike/logscale-community-content/issues).
