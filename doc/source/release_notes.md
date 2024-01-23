# Release Notes

Note for handling releases.

## Version Numbers

EMD tries very hard to follow the [PEP 440](https://www.python.org/dev/peps/pep-0440/) versioning scheme. In brief, we version numbers follow a vX.Y.Z format where:

1. X - Major version: Huge additions, major checkpoints in development.
2. Y - Minor version: Larger additions, limited API changes if necessary.
3. Z - Patch: Tweaks, documentation, fixes and small, isolated additions. No API changes 

Most releases will be patches.

Unreleased work in progress will have a version number of the *next Minor release* with `.dev0` as the patch number. For instance, if we are making a release for `v0.5.3` then the `master` branch will be set to `v0.6.dev0`

## General Release Process

This is the general process for making a new EMD release.

#### Make a release branch

All releases should occur in their own branch. The version number changes
should only appear in this branch and will be reset before merging back to
master.

Can make a local branch

    git checkout -b bump_to_v0.5.2

or create a branch directly on gitlab

#### Update versions

Update version in:

    setup.py - MUST DO THIS ONE!
    doc/source/conf.py
    doc/source/install.rst
    changelog.md
    doc/source/_templates/version_switcher.html

#### Build new version

    make clean
    make all

and check `emd.__version__` is as expected.

#### Push branch to gitlab.com

Commit changes and push to bump branch on gitlab.com. Make sure that branch has associated Merge Request.

**ENSURE TESTS PASS before proceeding!!**

#### Tag release

Create new git tag from current state with an obvious commit message

    git tag -a v0.1.0 -m "Initial release"
    git tag -a v0.5.2 -m "Bump to v0.5.2"

#### Push tagged release

Push new git tag to gitlab.com

    git push origin v0.1.0

Check tagged version is under [Repository->Tags](https://gitlab.com/emd-dev/emd/-/tags) - version should be present with correct number and pass tests

#### Build distribution

Run builds on local version - **ensuring that you are on tagged commit**

    python setup.py sdist
    python setup.py bdist_wheel --universal

#### Upload to PyPI

Upload version, have PyPI username and password to hand

    twine upload --skip-existing dist/*

#### Reset versions to development release

Update version to `.dev0` in:

    setup.py
    doc/source/conf.py
    doc/source/install.rst
    changelog.md
    doc/source/_templates/version_switcher.html

#### Make new version

    make all

#### Merge to master

Commit final changes and push back to branch. Check versions match development release and merge.


## Marge requests

Details on handling Merge Requests from a developers perspective. A simple MR
can be merged directly from a fork of EMD whereas a more complex set of changes
may need to be moved to a branch directly on `emd-dev/emd` - this allows for
developers to more easily contribute to the branch before merging.

### Method 1 - Simple MR from fork

1) create fork of emd
2) make any changes in a branch
3) ensure that runners are enabled
"Settings -> CI/CD -> Runners -> Shared Runners" should be set on
4) ensure that pipeline results are public
"Settings -> CI/CD -> Public Pipelines" should be ticked
5) Make sure that tests are passing
6) Make merge request from fork repo
"Repository -> Branches" click 'Merge request" next to corresponding branch.

If absolutley necessary, a developer can push to a branch on someone elses
fork. Best to avoid this unless you're already working together though.

1) fetch branch in question

    git fetch "git@gitlab.com:ContributerName/emd.git" new_branch

2) checkout that branch

    git checkout -b "ContributerName/emd-new_branch" FETCH_HEAD

3) rename branch to match remote (optional but recommended)

    git branch -m new_branch

4) add remote of the fork contributing the MR

    git remote add ContributerName https://gitlab.com/ContributerName/emd.git

5) Set upstream of local branch to correct branch on contributing fork

    git branch new_branch --set-upstream-to ContributerName/new_branch

6) check everything is in order

    git remote update
    git status

7) Make sure you have approval to push to branch. Will likely need to be added as a contributer to the fork project.
8) do some work and push it

### Method 2 - MR from local branch

1) User opens an issue requesting a developement branch
2) Developer adds a MR associated with the issue
3) User requests to merge their Fork with the developement branch
4) User and developer can then contribute to that branch together until merge is ready

# Approving an MR
1) Do the tests pass?
2) Is documentation sufficient and clear?
3) Any updates to tutorials needed?
4) Changelog updated with reference to MR/branch and authors?
