---
title: Contributor Guidelines
---

# Contributor Guidelines

## Getting Started

Third-party patches are key to making Jenkins on DC/OS the best way to run
an efficient CI system. We want to keep it as easy as possible to contribute
changes that improve this project, or get it working in your environment. There
are a few guidelines we'd like contributors to follow to ensure a consistent
experience for everyone involved.

## Submitting Changes to Jenkins

  * A [GitHub pull request][github-pr-docs] is the preferred way of submitting
  patch sets.
  * Any changes in the public API or behavior must be reflected in the project
  documentation.
  * Pull requests should include appropriate additions to the test suite (if
  applicable).
  * If the change is a bugfix, then the added tests must fail without the patch
  as a safeguard against future regressions.


## Style

Before submitting your pull request, please consider:

  * Checking for unnecessary whitespace: this can be accomplished by running
  `git diff --check`. All tabs should be expanded to spaces; hard tabs are not
  permitted.
  * Please keep line length to around 79-80 characters. We understand this
  isn't always practical; just use your best judgement.
  * Include comments where appropriate.
  * Any changes to the Python code should follow [PEP-8][pep-8-style].
  * Please, no additional copyright statements or licenses in source files.

Additionally, we would prefer the following format for commit messages:

```
A brief summary, no more than 50 characters

Prior to this patch, there wasn't an example of a commit message in the
contributing documentation. This had the side effect of the user having
no idea what an acceptable commit message might look like.

This commit fixes this problem by introducing a real-world example to
the contributing documentation.
```

[github-pr-docs]: https://help.github.com/articles/using-pull-requests
[pep-8-style]: https://www.python.org/dev/peps/pep-0008/
