# Changelog

## [unreleased]

### Breaking

* blag does not use default fallback templates anymore and will return an error
  if it is unable to find required templates, e.g. in `templates/`.

  Users upgrading from older versions can either run `blag quickstart` (don't
  forget to backup your `config.ini` or copy the templates from blag's
  resources (the resource path is shown in the error message).

  New users are not affected as `blag quickstart` will generate the needed
  templates.

* Split former archive page which served as index.html into "index" and
  "archive", each with their own template, respectively. Index is the landing
  page and shows by default only the latest 10 articles. Archive shows the full
  list of articles.

  If you used custom templates,
    * you should create an "index.html"-template (take blag's default one as a
      starting point)
    * you may want to include the new "/archive.html" link somewhere in your
      navigation

### Changed

* blag comes now with a simple yet good looking default theme that supports
  syntax highlighting and a light- and dark theme.


## [1.5.0] - 2023-04-16

* moved to pyproject.toml
* added python 3.11 to test suite
* break out lint and mypy from test matrix and only run on linux- and latest
  stable python to make it a bit more efficient
* added dependabot check for github actions
* updated dependencies:
  * mypy 1.2.0
  * types-markdown 3.4.2.1
  * pytest-cov 4.0.0
  * sphinx 5.3.0
  * pytest 7.3.0
  * flake8 6.0.0
  * twine 4.0.2
  * wheel 0.40.0

## [1.4.1] - 2022-09-29

* applied multi-arch fix by debian-janitor
* updated dependencies:
  * pytest 7.1.3
  * sphinx 5.2.1
  * types-markdown 3.4.2

## [1.4.0] - 2022-09-01

* added type hints and mypy --strict to test suite
* improved default template
* updated dependencies:
  * markdown 3.4.1
  * pygments 2.13.0
  * flake 5.0.4
  * twine 4.0.1
  * sphinx 5.1.1

## [1.3.2] - 2022-06-29

* Added --version option
* added --verbose option, that increases the loglevel to 'debug'
* Improved quickstart:
  * respective default answers will be written to config if user provided no
    answer
  * added tests for quickstart
* Added some test cases for the MarkdownLinktreeProcessor

## [1.3.1] - 2022-06-10

* fixed man page

## [1.3.0] - 2022-06-09

* debianized package
* Small fix in makefile
* updated dependencies:
  * pytest 7.1.2
  * sphinx 5.0.0
  * twine 3.7.1
  * wheel 0.37.1
  * markdown 3.3.7
  * jinja 3.1.2
  * pygments 2.12.0

## [1.2.0] - 2021-11-06

* `make serve` now rebuilds immediately once after called to avoid serving
  stale files
* updated dependencies:
  * feedgenerator 2.0.0
  * jinja2 3.0.1
  * pytest-cov 3.0.0
  * flake8 4.0.1
  * twine 3.5.0

## [1.1.0] - 2021-10-06

* added Python 3.10 to list of supported versions to test against
* added dependabot to github workflows
* updated various dependencies:
  * pygments 2.10.0
  * sphinx 4.2.0
  * twine 3.4.2
  * wheel 0.37.0
  * pytest 6.2.5

## [1.0.0] - 2021-08-18

* first 1.0 release!
* bump requirements of feedgenerator to 1.9.2. this version uses the
  description to provide a subtitle for the feed

## [0.0.9] - 2021-06-22

* updated to jinja 3.0
* updated to sphinx 4.0
* added link to changelog
