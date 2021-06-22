# About

A collection of tools Libro.org uses to produce its ebooks, including basic setup of ebooks, text processing, and build tools.

Forked from [Standard Ebooks tools](https://github.com/standardebooks/tools).

Installing this toolset using `pipx` makes the `libro` command line executable available. Its various commands are described below, or you can use `libro help` to list them.

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

# Project status

|          Feature          | Status |
| :-----------------------: | ------ |
| adapt commands to Spanish | WIP    |
|    Libro.org skeleton     | WIP    |
|     shell completions     | TO-DO  |

# Installation

The toolset requires Python >= 3.6.

To install the toolset locally for development and debugging, see [Installation for Developers](#installation-for-developers).

## Ubuntu 20.04 (Trusty) users

```shell
# Install some pre-flight dependencies.
sudo apt install -y calibre default-jre git python3-dev python3-pip python3-venv

# Install pipx.
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install the toolset.
pipx install libro-org
```

### Optional: Install shell completions

```shell
# Install ZSH completions.
sudo ln -s $HOME/.local/pipx/venvs/standardebooks/lib/python3.*/site-packages/se/completions/zsh/_se /usr/share/zsh/vendor-completions/_se && hash -rf && compinit

# Install Bash completions.
sudo ln -s $HOME/.local/pipx/venvs/standardebooks/lib/python3.*/site-packages/se/completions/bash/se /usr/share/bash-completion/completions/se

# Install Fish completions.
sudo ln -s $HOME/.local/pipx/venvs/standardebooks/lib/python3.*/site-packages/se/completions/fish/se $HOME/.config/fish/completions/se.fish
```

## Fedora users

```shell
# Install some pre-flight dependencies.
sudo dnf install calibre git java-1.8.0-openjdk python3-devel vim

# Install pipx.
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install the toolset.
pipx install libro-org
```

### Optional: Install shell completions

```shell
# Install ZSH completions.
sudo ln -s $HOME/.local/pipx/venvs/standardebooks/lib/python3.*/site-packages/se/completions/zsh/_se /usr/share/zsh/vendor-completions/_se && hash -rf && compinit

# Install Bash completions.
sudo ln -s $HOME/.local/pipx/venvs/standardebooks/lib/python3.*/site-packages/se/completions/bash/se /usr/share/bash-completion/completions/se

# Install Fish completions.
sudo ln -s $HOME/.local/pipx/venvs/standardebooks/lib/python3.*/site-packages/se/completions/fish/se $HOME/.config/fish/completions/se.fish
```

## macOS users (up to macOS 10.15)

These instructions were tested on macOS 10.12 to 10.16, on Intel macs.

1. Install the [Homebrew package manager](https://brew.sh). Or, if you already have it installed, make sure it’s up to date:

   ```shell
   brew update
   ```

2. Install dependencies:

   ```shell
   # Install some pre-flight dependencies.
   brew install cairo calibre git openjdk pipx python
   pipx ensurepath
   sudo ln -sfn /usr/local/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk

   # Install the toolset.
   pipx install libro-org

   # Optional: Bash users who have set up bash-completion via brew can install tab completion.
   ln -s $HOME/.local/pipx/venvs/standardebooks/lib/python3.*/site-packages/se/completions/bash/se $(brew --prefix)/etc/bash_completion.d/se

   # Optional: Fish users can install tab completion.
   ln -s $HOME/.local/pipx/venvs/standardebooks/lib/python3.*/site-packages/se/completions/fish/se $HOME/.config/fish/completions/se.fish
   ```

## OpenBSD 6.6 Users

These instructions were tested on OpenBSD 6.6, but may also work on the 6.5 release as well.

1.  Create a text file to feed into `pkg_add` called `~/standard-ebooks-packages`. It should contain the following:

        ```shell
        py3-pip--
        py3-virtualenv--
        py3-gitdb--
        jdk--%11
        calibre--
        git--
        vim--
        ```

    Optionally, replace `vim--` with `vim--gtk3` to include gvim for its Unicode editing features.

2.  Install dependencies using `doas pkg_add -ivl ~/standard-ebooks-packages`. Follow linking instructions provided by `pkg_add` to save keystrokes, unless you want to have multiple python versions and pip versions. In my case, I ran `doas ln -sf /usr/local/bin/pip3.7 /usr/local/bin/pip`.

3.  Add `~/.local/bin` to your path.

4.  Run `pip install --user pipx`

5.  If you’re using `ksh` from base and have already added `~/.local/bin`, you can skip `pipx ensurepath` because this step is for `bash` users.

6.  The rest of the process is similar to that used on other platforms:

    ```shell
    # Install the toolset.
    pipx install libro-org
    ```

## Installation for developers

If you want to work on the toolset source, it’s helpful to tell `pipx` to install the package in “editable” mode. This will allow you to edit the source of the package live and see changes immediately, without having to uninstall and re-install the package.

To do that, follow the general installation instructions above; but instead of doing `pipx install libro-org`, do the following:

```shell
git clone https://github.com/Libro-Org/tools.git
pipx install --editable ./tools
```

Now the `libro` binary is in your path, and any edits you make to source files in the `tools/` directory are immediately reflected when executing the binary.

### Running commands on the entire corpus

As a developer, it’s often useful to run an `libro` command like `libro lint` or `libro build` on the entire corpus for testing purposes. This can be very time-consuming in a regular invocation (like `libro lint /path/to/ebook/repos/*`), because each argument is processed sequentially. Instead of waiting for a single invocation to process all of its arguments sequentially, use [GNU Parallel](https://www.gnu.org/software/parallel/) to start multiple invocations in parallel, with each one processing a single argument. For example:

```shell
# Slow, each argument is processed in sequence
se lint /path/to/ebook/repos/*

# Fast, multiple invocations each process a single argument in parallel
export COLUMNS; parallel --keep-order se lint ::: /path/to/ebook/repos/*
```

The toolset tries to detect when it’s being invoked from `parallel`, and it adjusts its output to accomodate.

We export `COLUMNS` because `libro lint` needs to know the width of the terminal so that it can format its tabular output correctly. We pass the `--keep-order` flag to output results in the order we passed them in, which is useful if comparing the results of multiple runs.

### Linting with `pylint` and `mypy`

Before we can use `pylint` or `mypy` on the toolset source, we have to inject them into the venv `pipx` created for the `libro-org` package:

```shell
pipx inject libro-org pylint mypy
```

Then make sure to call the `pylint` and `mypy` binaries that `pipx` installed in the `libro-org` venv, _not_ any other globally-installed binaries:

```shell
cd /path/to/tools/repo
$HOME/.local/pipx/venvs/libro-org/bin/pylint se
```

### Testing with `pytest`

Similar to `pylint`, the `pytest` command can be injected into the venv `pipx` created for the `standardebooks` package:

```shell
pipx inject libro-org pytest
```

The tests are executed by calling `pytest` from the top level or your tools repo:

```shell
cd /path/to/tools/repo
$HOME/.local/pipx/venvs/libro-org/bin/pytest
```

#### Adding tests

Tests are added under the `tests` directory. Most of the tests are based around the idea of having “golden” output files. Each command is run against a set of input files and then the resulting output files are compared against the resulting golden files. The test fails if the output files do not match the golden files. The data files can be found in the `tests/data` directory.

A custom test flag `--save-golden-files` has been added to automatically update the the golden files for the tests (in an `out` directory for the command).

The usual test development process is:

1. Update `in` files with new test data and/or change the command implementation.
2. Run `pytest` and see some tests fail.
3. Run `pytest --save-golden-files` and then diff the data directory to ensure that the `out` files are as expected.
4. Commit changes (including new `out` contents).

Another custom test flag `--save-new-draft` is also available. This flag is used to update the book skeleton, generated by the `libro create-draft` command, that is used as input for the other tests. Whenever the draft contents change (e.g. edits to the `core.css` file) the `tests/data/draft` files should be updated by calling `pytest --save-new-draft`.

### Code style

- In general we follow a relaxed version of [PEP 8](https://www.python.org/dev/peps/pep-0008/). In particular, we use tabs instead of spaces, and there is no line length limit.

- Always use the `regex` module instead of the `re` module.

# Help wanted

We need volunteers to take the lead on the following goals:

- Add more test cases to the test framework.

- Figure out if it’s possible to install Bash/ZSH completions using setup.py, _without_ root; this may not be possible?

- Writing installation instructions for Bash and ZSH completions for MacOS.

- Currently we install the whole Calibre package, which is very big, but it’s only used to convert epub to azw3. Can we inline Calibre’s azw3 conversion code in the `./vendor/` directory, to avoid having to install the entire package as a big dependency?

# Tool descriptions

- ### `libro build`

  Build an ebook from a Standard Ebook source directory.

- ### `libro build-images`

  Build ebook cover and titlepage images in a Standard Ebook source directory and place the output in DIRECTORY/src/epub/images/.

- ### `libro clean`

  Prettify and canonicalize individual XHTML, SVG, or CSS files, or all XHTML, SVG, or CSS files in a source directory. Note that this only prettifies the source code; it doesn’t perform typography changes.

- ### `libro compare-versions`

  Use Firefox to render and compare XHTML files in an ebook repository. Run on a dirty repository to visually compare the repository’s dirty state with its clean state. If a file renders differently, place screenshots of the new, original, and diff (if available) renderings in the current working directory. A file called diff.html is created to allow for side-by-side comparisons of original and new files.

- ### `libro create-draft`

  Create a skeleton of a new Standard Ebook.

- ### `libro dec2roman`

  Convert a decimal number to a Roman numeral.

- ### `libro extract-ebook`

  Extract an EPUB, MOBI, or AZW3 ebook into ./FILENAME.extracted/ or a target directory.

- ### `libro find-mismatched-diacritics`

  Find words with mismatched diacritics in Standard Ebook source directories. For example, `cafe` in one file and `café` in another.

- ### `libro help`

  List available SE commands.

- ### `libro hyphenate`

  Insert soft hyphens at syllable breaks in an XHTML file.

- ### `libro interactive-sr`

  Use Vim to perform an interactive search and replace on a list of files. Use y/n/a to confirm (y) or reject (n) a replacement, or to replace (a)ll.

- ### `libro lint`

  Check for various Standard Ebooks style errors.

- ### `libro make-url-safe`

  Make a string URL-safe.

- ### `libro modernize-spelling`

  Modernize spelling of some archaic words, and replace words that may be archaically compounded with a dash to a more modern spelling. For example, replace `ash-tray` with `ashtray`.

- ### `libro prepare-release`

  Calculate work word count, insert release date if not yet set, and update modified date and revision number.

- ### `libro print-manifest`

  Print the <manifest> element for the given Standard Ebooks source directory to standard output, for use in that directory’s content.opf.

- ### `libro print-spine`

  Print the <spine> element for the given Standard Ebooks source directory to standard output, for use in that directory’s content.opf.

- ### `libro print-title`

  Print the expected value for an XHTML file’s `<title>` element.

- ### `libro print-toc`

  Build a table of contents for an SE source directory and print to stdout.

- ### `libro recompose-epub`

  Recompose a Standard Ebooks source directory into a single HTML5 file, and print to standard output.

- ### `libro renumber-endnotes`

  Renumber all endnotes and noterefs sequentially from the beginning.

- ### `libro reorder-endnotes`

  Increment the specified endnote and all following endnotes by 1.

- ### `libro roman2dec`

  Convert a Roman numeral to a decimal number.

- ### `libro semanticate`

  Apply some scriptable semantics rules from the Standard Ebooks semantics manual to a Standard Ebook source directory.

- ### `libro split-file`

  Split an XHTML file into many files at all instances of `<!--se:split-->`, and include a header template for each file.

- ### `libro titlecase`

  Convert a string to titlecase.

- ### `libro typogrify`

  Apply some scriptable typography rules from the Standard Ebooks typography manual to a Standard Ebook source directory.

- ### `libro unicode-names`

  Display Unicode code points, descriptions, and links to more details for each character in a string. Useful for differentiating between different flavors of spaces, dashes, and invisible characters like word joiners.

- ### `libro version`

  Print the version number and exit.

- ### `libro word-count`

  Count the number of words in an HTML file and optionally categorize by length.

- ### `libro xpath`

  Print the results of an xpath expression evaluated against a set of XHTML files. The default namespace is removed.

# What a Libro.org source directory looks like

Many of these tools act on Libro.org source directories. Such directories have a consistent minimal structure:

    .
    |-images/
    |--cover.jpg
    |--cover.source.jpg
    |--cover.svg
    |--titlepage.svg
    |-src/
    |--epub/
    |---css/
    |----core.css
    |----local.css
    |----se.css
    |---images/
    |----cover.svg
    |----titlepage.svg
    |---text/
    |----colophon.xhtml
    |----imprint.xhtml
    |----titlepage.xhtml
    |----uncopyright.xhtml
    |---content.opf
    |---onix.xml
    |---toc.xhtml
    |--META-INF/
    |---container.xml
    |--mimetype
    |-LICENSE.md

`./images/` contains source images for the cover and titlepages, as well as ebook-specific source images. Source images should be in their maximum available resolution, then compressed and placed in `./src/epub/images/` for distribution.

`./src/epub/` contains the actual epub files.
