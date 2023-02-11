# Contributing to this repository <!-- omit in toc -->


_Welcome!_ We're excited you want to contribute to the LogScale Community Content

Please review this document for details regarding getting started with your first contribution, file formats and standards, and our Pull Request process. If you have any questions, please let us know by
posting your question in the [Issues](https://github.com/CrowdStrike/logscale-community-content/issues).

**Before you begin**: Have you read the [Code of Conduct](https://github.com/CrowdStrike/logscale-community-content/blob/main/CODE_OF_CONDUCT.md)?

The Code of Conduct helps us establish community norms and how they'll be enforced.

- [How you can contribute](#how-you-can-contribute)
    + [Bug reporting](#bug-reporting-is-handled-using-github-issues)
    + [All other discussions](#discussions-are-used-for-questions-suggestions-and-feedback)
- [Pull Requests](#pull-requests)
    + [Contributor dependencies](#additional-contributor-package-requirements)
    + [Unit testing and Code coverage](#unit-testing-and-code-coverage)
    + [Code Quality and Style (Linting)](#code-quality-and-style-linting)
    + [Breaking changes](#breaking-changes)
    + [Branch targeting](#branch-targeting)
    + [Pull Request Template](#pull-request-template)
    + :warning: [Pull Request Restrictions](#pull-request-restrictions)
    + [Approval and Merging](#approval-and-merging)
    + [Releases](#releases)
- [Suggestions](#suggestions)

## How you can contribute
- See something? Say something! Submit a [bug report](https://github.com/CrowdStrike/logscale-community-content/issues) to let the community know what you've experienced or found. Bonus points if you suggest possible fixes or what you feel may resolve the issue. 
- Submit a [Pull Request](#pull-requests)

### Bug reporting is handled using GitHub issues
We use [GitHub issues](https://github.com/CrowdStrike/falconpy/issues) to track:

+ [bugs](https://github.com/CrowdStrike/falconpy/issues?q=is%3Aissue+label%3A%22bug+%3Abug%3A%22) (`BUG`)
+ [documentation](https://github.com/CrowdStrike/falconpy/issues?q=is%3Aissue+label%3A%22documentation+%3Abook%3A%22) and [linking](https://github.com/CrowdStrike/falconpy/issues?q=is%3Aissue+label%3A%22broken+link+%3Alink%3A%22) issues (`DOC`, `LINK`)
+ [enhancements](https://github.com/CrowdStrike/falconpy/issues?q=is%3Aissue+label%3A%22enhancement+%3Astar2%3A%22) (`ENH`)
+ [security concerns](https://github.com/CrowdStrike/falconpy/issues?q=is%3Aissue+label%3Asecurity) (`SEC`)

[Report Issue](https://github.com/CrowdStrike/falconpy/issues/new)

---

## Pull Requests
In order for your pull request to be merged, it must pass code style and unit testing requirements. Pull requests that do not receive responses to feedback or requests for changes will be closed.

### All contributions will be submitted under the Unlicense license
When you submit code changes, your submissions are understood to be under the same Unlicense [license](LICENSE) that covers the repository. 
If this is a concern, contact the maintainers before contributing.

### Code Quality and Style (Linting)
[![Check Docstrings](https://github.com/CrowdStrike/falconpy/actions/workflows/pydocstyle.yml/badge.svg)](https://github.com/CrowdStrike/falconpy/actions/workflows/pydocstyle.yml)
[![Flake8](https://github.com/CrowdStrike/falconpy/actions/workflows/flake8.yml/badge.svg)](https://github.com/CrowdStrike/falconpy/actions/workflows/flake8.yml)
[![Pylint](https://github.com/CrowdStrike/falconpy/actions/workflows/pylint.yml/badge.svg)](https://github.com/CrowdStrike/falconpy/actions/workflows/pylint.yml)

All submitted code must meet minimum linting requirements. We use the Flake8 framework for our lint specification.
+ All code that is included within the installation package must pass linting workflows when the Pull Request checks have completed.
    - We use `flake8`, `CodeQL`, `pydocstyle` and `pylint` to power our linting workflows. 
    - You will be asked to correct linting errors before your Pull Request will be approved.
+ Unit tests do not need to meet this requirement, but try to keep linting errors to a minimum.
+ Samples are checked for linting, but failures will not stop builds at this time.
+ Refer to the `lint.sh` script within the util folder to review our standard linting parameters.
> You can quickly check the linting for all code within the src folder by executing the command `util/lint.sh` from the root of the project directory.

More information about _Flake8_ can be found [here](https://flake8.pycqa.org/en/latest/).

More information about _pydocstyle_ can be found [here](http://www.pydocstyle.org/en/stable/).

More information about _Pylint_ can be found [here](https://www.pylint.org/).

### Breaking changes
In an effort to maintain backwards compatibility, we thoroughly unit test every Pull Request for all versions of Python we support. These unit tests are intended to catch general programmatic errors, possible vulnerabilities (via `bandit` and `CodeQL`) and _potential breaking changes_. 

> If you have to adjust a unit test locally in order to produce passing results, there is a possibility you are working with a potential breaking change.

Please fully document changes to unit tests within your Pull Request. If you did not specify "Breaking Change" on the punch list in the description, and the change is identified as possibly breaking, this may delay or prevent approval of your PR.

### Branch targeting
_Please do not target the `main` branch with your Pull Request unless it is the only branch or you are directed to do so by a maintainer_. 

All pull requests should target a new unique branch using a naming standard that is appropriate.  

Depending on the nature of your pull request, you may be contacted by a maintainer and asked to target a new branch specific to your submission.

### Pull Request template
Please use the pull request template provided, making sure the following details are included in your request:
+ Is this a breaking change?
+ Are all new or changed code paths covered by unit testing?
+ A complete listing of issues addressed or closed with this change.
+ A complete listing of any enhancements provided by this change.
+ Any usage details developers may need to make use of this new functionality.
    - Does additional documentation need to be developed beyond what is listed in your Pull Request?
+ Any other salient points of interest.

### Pull Request restrictions
Please review this list and confirm none of the following concerns exist within your request.
Pull requests containing any of these elements will be prevented from merging to the code base and may be closed.

| Concern | Restriction |
| :--- | :--- |
| **Scripts** | Limited exceptions to be reviewed by maintainers on a case by case basis. |
| **Binaries** | Compiled binaries, regardless of intent should not be included in the code base or in samples. |
| **Disparaging references to 3rd party vendors in source or content** | We are here to collaborate regarding LogScale Community Content, not bash the work of others. |
| **Inappropriate language, comments or references found within source or content** | Comments (and comment art) must not detract from code legibility or impact overall package size. **All** content published to this repository (source or otherwise) must follow the [Code of Conduct](https://github.com/CrowdStrike/falconpy/blob/main/CODE_OF_CONDUCT.md). |
| **Intellectual property that is not yours** | Copywrited works, trademarks, source code or image assets belonging to others should not be posted to this repository whatsoever. CrowdStrike assets which are already released into the Public Domain will be accepted as long as their usage meets other restrictions, the rules specified in the [Code of Conduct](https://github.com/CrowdStrike/logscale-community-content/blob/main/CODE_OF_CONDUCT.md), and the guidelines set forth in the [CrowdStrike Brand Guide](https://crowdstrikebrand.com/brand-guide/). |
| **Relative links in README files** | This impacts our package deployment as these files are consumed as part of the build process. All link and image references within README files must contain the full URL. |

### Approval and Merging
All Pull Requests must be approved by at least one maintainer. Once approved, a maintainer will perform the merge and execute any backend 
processes related to package deployment. 

At this point in time, `main` is a protected branch.

To read more about the FalconPy code review and packaging cycle, please review the contents of [this page](https://github.com/CrowdStrike/falconpy/blob/main/docs/PACKAGING.md).

## Suggestions
If you have suggestions on how this process could be improved, please let us know by [starting a new discussion](https://github.com/CrowdStrike/falconpy/discussions).
