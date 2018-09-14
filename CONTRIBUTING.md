# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways...

## Types of Contributions

### Report Bugs

Report bugs at [Manjaro Gitlab](https://gitlab.manjaro.org/fhdk/application-utility/issues).

If you are reporting a bug, please include:

- Your Manjaro Edition.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the Gitlab issues for bugs. Anything tagged with "bug" is open to whoever wants to implement it.

### Implement Features

Look through the Gitlab issues for features. Anything tagged with "feature" is open to whoever wants to implement it.

### Write Documentation

The app could always use more documentation, whether as part of the official  docs, in docstrings, or even on the web in blog posts, articles, and such.

### Translations

Help us to ship  in your language by help translating.

### Submit Feedback

The best way to send feedback is to file an issue at [Manjaro Gitlab](https://gitlab.manjaro.org/fhdk/application-utility/issues).

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `application-utility` for local development.

* Fork the `application-utility` repo on Manjaro Gitlab.
* Clone your fork locally:
    
```
$ git clone https://gitlab.manjaro.org/your-name-here/application-utility.git
```
    
* Install your local copy into a virtualenv. Assuming you have [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) installed, this is how you set up your fork for local development
* Remember to `source /usr/bin/virtualenvwrapper.sh` to get the virtualenv CLI

```    
$ mkvirtualenv 
$ cd /
$ python setup.py develop
```

* Create a branch for local development:

```
$ git checkout -b name-of-your-bugfix-or-feature
```

   Now you can make your changes locally.

* When you're done making changes, commit your changes and push your branch to gitlab:

```
$ git add
$ git commit -m "Your detailed description of your changes."
$ git push origin name-of-your-bugfix-or-feature
```

* Submit a pull request through the Gitlab website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

* The pull request should include tests.
* If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.md.

## Tips


## Developing environment

* An editor of choice e.g.
   * Visual Studio Code `yay -S visual-studio-code`
   * PyCharm Community `pacman -Syu pycharm-community`
* Pandoc converter `pacman -Syu pandoc`
* Python environment

```
$ git clone https://gitlab.manjaro.org/fhdk/application-utility.git
$ cd 
$ sudo pacman -Syu python-pip python-virtualenvwrapper
$ mkvirtualenv application-utility
$ python setup.py develop
$ pip install mkdocs babel
```
