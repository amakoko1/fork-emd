# Changelog

Changes and updates to EMD are tracked by version on this page.  The format of
this changelog is (mostly) based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this the EMD package uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Changes should be categorised under the following types:

- **Added** for new features.
- **Changed** for changes in existing functionality.
- **Deprecated** for soon-to-be removed features.
- **Removed** for now removed features.
- **Fixed** for any bug fixes.
- **Security** in case of vulnerabilities.

Where appropriate, links to specific Issues & Merge Requests on [our gitlab page](https://gitlab.com/emd-dev/emd).


## Development Version
Work in progress...

    git clone https://gitlab.com/emd-dev/emd.git

### Changed
- Drop version pin on numpy [!88](https://gitlab.com/emd-dev/emd/-/merge_requests/88)
- Move imports to optimise speed of initial imports [!88](https://gitlab.com/emd-dev/emd/-/merge_requests/88)
- Change version management to use dedicated version file and drop pkg_resources [!88](https://gitlab.com/emd-dev/emd/-/merge_requests/88)

### Removed
- Support for python 3.6 (https://endoflife.date/python)

### Fixed
- Support for unequal segment lengths in assess_harmonic_criteria [!89](https://gitlab.com/emd-dev/emd/-/merge_requests/89)

---

# Stable Versions

## 0.5.5

    pip install emd==0.5.5
Released 2022-05-27

### Fixed
- Latex rendering in website an a couple of doc fixes.

---

## 0.5.4

    pip install emd==0.5.4
Released 2022-05-20

### Added
- Functions for assessing the harmonic relationship between IMFs [!82](https://gitlab.com/emd-dev/emd/-/merge_requests/82)

### Fixed
- Documentation and bug fixes for Hilbert-Marginal spectrum [!77](https://gitlab.com/emd-dev/emd/-/merge_requests/77)
- Fix logic in wrap_verbose to avoid pointless 'level unchanged' warning [!79](https://gitlab.com/emd-dev/emd/-/merge_requests/79/diffs)
- Add additional input checking and nan-avoidance in emd.imftools.wrap phase [!79](https://gitlab.com/emd-dev/emd/-/merge_requests/79/diffs)
- Equation brakets typo in Abreu2010 simulator & docstring improvements [!81](https://gitlab.com/emd-dev/emd/-/merge_requests/81)

### Changed
- New imf plotting tool - puts figure into single axes and adds more customisation [!78](https://gitlab.com/emd-dev/emd/-/merge_requests/78)
- Added minimum cycle length option to cycle detection and additional checks to phase_align [!80](https://gitlab.com/emd-dev/emd/-/merge_requests/80)

---

## 0.5.3

    pip install emd==0.5.3
Released 2022-02-11

### Added

- Support for python3.10 and numpy<1.21 [!76](https://gitlab.com/emd-dev/emd/-/merge_requests/76)
- Additional installation instructions for conda-forge and developer details for making releases on website.
- Functions for assessing sift quality - pseudo\_mode\_mixing\_index and check\_decreasing\_freq [5e59dc2f](https://gitlab.com/emd-dev/emd/-/commit/5e59dc2fe6b93145b8fed6eaf58d02b732c68afa)
- Work in progress started on circular statistics

### Changed

- Restructure of low-level functions to improve internal importing chain [f80fb824](https://gitlab.com/emd-dev/emd/-/commit/0f4893e25c35266f55ef251cbe50525ff2761603)
  - imftools submodule containing general purpose functions intended to be run on IMFs and their instantaneous frequency stats.
  - simulations submodule containing data simulators previously in utils and the harmonic tool
  - \_sift\_core submodule containing the low level sifting functions that might be imported into other submodules.
  - Website and documentation updated to reflect changes

### Removed

- utils submodule deleted and functions moved into imftools, simulate, and support.

### Fixed

- Hilbert Marginal spectrum bug fixes [#60](https://gitlab.com/emd-dev/emd/-/issues/60)
- Fix y-axis scaling in Hilbert-Huang tutorial [8cc65488](https://gitlab.com/emd-dev/emd/-/merge_requests/76/diffs?commit_id=8cc65488d0b337535266d566823bdbd269c9ab97)
- Correct extrema now returned when finding troughs in 'rilling' mode [5dd9aff2](https://gitlab.com/emd-dev/emd/-/commit/5dd9aff2b2c1088484caf00ae6fd6d7c27defa0b)

---

## 0.5.2

    pip install emd==0.5.2
Released 2022-01-13

### Added

- New tutorial on harmonic structures and instantaneous frequency [!74](https://gitlab.com/emd-dev/emd/-/merge_requests/74)

---

## 0.5.1

    pip install emd==0.5.1
Released 2021-12-17

### Notes

This release fixes a bug with the initial v0.5.0 release.

---

## 0.5.0

    pip install emd==0.5.0
Released 2021-12-17

### Notes
This release contains several breaking changes in the emd.spectra submodule
particularly in the emd.spectra.hilberthuang and emd.spectra.holospectrum
functions. Please see the relevant docstrings for a review of new API.

### Added
- Implementation of the Iterated Mask Sift from @marcofabus [!69](https://gitlab.com/emd-dev/emd/-/merge_requests/69)
- Support for Python 3.9 - requirements updated and test build added [!62](https://gitlab.com/emd-dev/emd/-/merge_requests/62)
- Dependancy on Sparse for spectrum computation (https://sparse.pydata.org/en/stable/) [!70](https://gitlab.com/emd-dev/emd/-/merge_requests/70)
- New citations page on website (and assorted website/reference fixups) [!60](https://gitlab.com/emd-dev/emd/-/merge_requests/60)

### Changed
- BREAKING: emd.spectra.hilberthuang and emd.spectra.holospectrum API changed, also now return frequency bin vectors. [!70](https://gitlab.com/emd-dev/emd/-/merge_requests/70)
- Major refector of spectrum code [!70](https://gitlab.com/emd-dev/emd/-/merge_requests/70)
- Major refactor of extrema padding underlying the sift [!71](https://gitlab.com/emd-dev/emd/-/merge_requests/71)

### Fixed
- Average over only the ensembles with the modal number of IMFs in ensemble_sift, previously there could be an error due to difference in nimfs between ensembles [!63](https://gitlab.com/emd-dev/emd/-/merge_requests/63)
- Fix pyyaml dependency for google-colab import [!64](https://gitlab.com/emd-dev/emd/-/merge_requests/64)
- Fix case where mask sift could drop some options [!66](https://gitlab.com/emd-dev/emd/-/merge_requests/66)
- Fix bug in energy ratio sift stopping method [95295a8c](https://gitlab.com/emd-dev/emd/-/merge_requests/71/diffs?commit_id=95295a8ca992a0df13597c39924af61eca7130bc)
- Fix bug in zero-crossing count mask frequency selection method [fe2605c2](https://gitlab.com/emd-dev/emd/-/merge_requests/71/diffs?commit_id=fe2605c2ca0730750912a1d5af1d2c52a27b142a)

### Removed
- emd.spectra.frequency_stats removed - replaced by emd.spectra.frequency_transform
- emd.spectra.hilberthuang_1d merged into emd.spectra.hilberthuang

## 0.4.0

    pip install emd==0.4.0
Released 2021-03-30

### Notes
Many changes in this revision come from the review process at [JOSS](https://github.com/openjournals/joss-reviews/issues/2977)

### Added
- New tutorials
  - Cross-frequency coupling [!52](https://gitlab.com/emd-dev/emd/-/merge_requests/52)
  - Why use EMD? [90a5b5e2](https://gitlab.com/emd-dev/emd/-/commit/90a5b5e2e4ffdd7634cf63e30836843c920fcaa3)
  - Tutorial on code speed [35ae8c82](https://gitlab.com/emd-dev/emd/-/commit/35ae8c82ab72b9c36d641eb4bef4d1ae7c53b0a5)
- Second layer mask sift function [65a05dd2](https://gitlab.com/emd-dev/emd/-/commit/65a05dd2cf1610508d13a68f6753094f07d67e48)
- Add html printing functionality for SiftConfig [5c57781e](https://gitlab.com/emd-dev/emd/-/commit/5c57781e2e8b92b8d2a7e00ceec8bde064bc412b)
- Update contribution and installation details on website - add accordions for better readability [!53](https://gitlab.com/emd-dev/emd/-/merge_requests/53)
- Add new plotting functionality for HHT and Holospectra [!53](https://gitlab.com/emd-dev/emd/-/merge_requests/53)
- Show warning when max_imfs is very high compared to length of time-series [4cd15291](https://gitlab.com/emd-dev/emd/-/commit/4cd15291c25e082cbb9ffb56a2c3812b6b3d391e)

### Changed
- Major refactor in handling of cycles analysis [!56](https://gitlab.com/emd-dev/emd/-/merge_requests/56)
  - Introduce Cycles class
  - Introduce \_cycles\_support module
- Renamed 'References' webpage to 'API' [d8fe93b5](https://gitlab.com/emd-dev/emd/-/commit/d8fe93b520c19ce45f3f5a73294074a4b1d75ce5)

### Fixed
- Widespread fixing of typos and mistakes in documentation & website [!52](https://gitlab.com/emd-dev/emd/-/merge_requests/52)
- Make docstrings pydocstyle compliant and add pydocstyle conventions [!53](https://gitlab.com/emd-dev/emd/-/merge_requests/53)
- Large number of pylint recommended fixes [271d7937](https://gitlab.com/emd-dev/emd/-/commit/271d793731fad64902f16323493ee06893002286)
- Indexing typo fixed in bin_by_phase [c5679432](https://gitlab.com/emd-dev/emd/-/commit/c5679432cfcd011965547144aaa936eee1405f62)
- Improve label alignments in plot_imfs [!54](https://gitlab.com/emd-dev/emd/-/merge_requests/56)

---

## 0.3.3

    pip install emd==0.3.3
Released 2021-02-04

### Added
- New function for computing summary stats from chains of cycles (from marcoFabus) [!46](https://gitlab.com/emd-dev/emd/-/merge_requests/46)

### Changed
- Major updates to tutorials [!40](https://gitlab.com/emd-dev/emd/-/merge_requests/40)
  - Binder notebooks added
  - New sifting tutorials added

### Fixed
- Replaced missing dependencies in setup.py [!42](https://gitlab.com/emd-dev/emd/-/merge_requests/42)

---

## 0.3.2

    pip install emd==0.3.2
Released 2020-11-29

### Added
- Add input array shape ensurance functions and start to use in sift & cycle submodules  [!26](https://gitlab.com/emd-dev/emd/-/merge_requests/26)
- Add more stopping criteria to sift module [!27](https://gitlab.com/emd-dev/emd/-/merge_requests/26)
  - Rilling et al and fixed iterations IMF stopping criteria
  - Energy threshold sift stopping criterion


### Changed
- Refactor some options extrema detection functions [!29](https://gitlab.com/emd-dev/emd/-/merge_requests/29)
- Sift throws an error if an IMF doesn't converge after a specified maximum number of iterations.
- Refactor mask generation in mask sift. Now specifies N masks of different phases and has options for parallel processing.
- SiftConfig yaml file also stores which type of sift the config is for [!35](https://gitlab.com/emd-dev/emd/-/merge_requests/35)
- 18% increase in testing coverage (to 75% total) [!30](https://gitlab.com/emd-dev/emd/-/merge_requests/30)

### Deprecated
- emd.spectra.frequency_stats renamed to emd.spectra.frequency_transform. Original func kept for now.

---

## 0.3.1

    pip install emd==0.3.1
Released 2020-09-06

### Added
- This changelog [!18](https://gitlab.com/emd-dev/emd/-/merge_requests/18)
- support.py submodule with some helper functions for checking installs and running tests [!20](https://gitlab.com/emd-dev/emd/-/merge_requests/20)
- envs subdir containing anaconda install environment config files [!21](https://gitlab.com/emd-dev/emd/-/merge_requests/21)
- Options for reading and writing sift configs to yaml format [!24](https://gitlab.com/emd-dev/emd/-/merge_requests/24)
- major update to webpage [!12](https://gitlab.com/emd-dev/emd/-/merge_requests/24)
  - Reformat page to bootstrap
  - Add & update the tutorials
  - New landing page

### Fixed
- Input array dimensions in phase_align clarified and fixed up [ef28b36c](https://gitlab.com/emd-dev/emd/-/commit/ef28b36cac8be7224280fd7ba02d25b3f084ab30)
- Extrema opts were dropped in get_next_imf [!23](https://gitlab.com/emd-dev/emd/-/merge_requests/23)

### Changed
- get_control_points internal refector [af153ed6](https://gitlab.com/emd-dev/emd/-/commit/af153ed606601f3963c125329c86710e47c06b45)

---

## 0.3.0

    pip install emd==0.3.0
Released on 2020-07-22

### Added
- get_cycle_stat refectored to allow general numpy and user-specified metrics to be computed
- Logger coverage increased, particularly in cycle.py
  - Logger exit message added

### Changed
- Major SiftConfig refactor - API & syntax now much cleaner

---

## 0.2.0

    pip install emd==0.2.0
Released 2020-06-05

### Added
- Tutorials on the sift, hilbert-huang and holospectrum analyses.
- Parabolic extrema interpolation
- Average envelope scaling in sift
- Testing expanded to include python 3.5, 3.6, 3.7 & 3.8


### Changed
- API in sift functions updated for compatabillity with new SiftConfig
  - Expose options for extrema padding to top level sift function
  - Sift relevant util functions moved into sift.py submodule
- Masked sift functions merged into single function
- get_cycle_chain refactor to cleaner internal syntax

---

## 0.1.0

    pip install emd==0.1.0
Released 2019-12-10

### Added
- Everything
