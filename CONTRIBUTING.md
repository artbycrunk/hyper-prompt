[![GitHub](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://raw.githubusercontent.com/artbycrunk/hyper-prompt/master/LICENSE)

## How to contribute 

So you want to contribute to the `hyper-prompt` project? Awesome! This document 
describes the guidelines you should follow when making contributions to the 
project.

### Getting started

* Make sure you have a [GitHub account](https://github.com/signup/free).
* Submit an issue on GitHub, assuming one does not already exist.
* Fork the [hyper-prompt](https://github.com/artbycrunk/hyper-prompt) repository on GitHub.

### Making changes

* Create a topic branch from where you want to base your work.
* Prefix your branch with ``feature/`` if you're working on a new feature.
* Include the issue number in your topic branch, e.g.  
    ``777-coolfix`` or ``feature/777-a-hot-feature``.
* Make commits of logical units.
* Make sure your commit messages are in the [proper format](
  http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)

  The summary must be no longer than 70 characters. Refer to any related 
  issues with e.g. ``Ref #777`` or ``Fixes #777`` at the bottom of the 
  commit message. Commit messages can use Markdown with the following 
  exceptions:
  * No HTML extensions.
  * Only indented code blocks (no ``` blocks).
  * Long links should be moved to the bottom if they make the text wrap or 
    extend past 72 columns.

* Make sure you have added the necessary tests for your changes.
* Run *all* the tests to assure nothing else was accidentally broken. See section beflow on running tests.

### Linting
We use `flake8` for linting, and the settings can be found here [flake8](.flake8)

### Formatting
This is optional. Use the following settings for `autopep8` or equivalent settings with the formatter of your choice:
VSC Python settings for formating:
```json
"python.formatting.provider": "autopep8",
"python.formatting.autopep8Args": [
    "--ignore", "E24,E121,E123,E125,E126,E221,E226,E266,E704,E265,E722,E501,E731,E306,E401,E302,E222,E303,E402,E305,E261,E262"
],
```

### Running tests
We use `pytest` for unittesting. Newer tests must go into the [tests](tests) directory.

###  Submitting changes
* Push your changes to a topic branch in your fork of the repository.
* If necessary, use ``git rebase -i <revision>`` to squash or reword commits
  before submitting a pull request.
* Submit a pull request to [hyper-prompt repository](https://github.com/artbycrunk/hyper-prompt)