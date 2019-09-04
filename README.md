# DBImport

## Information

This tool/prject is import json file class info fetch from De Anza College / Foothill College portal
to MongoDB database.

## Requirements

Python v3.6
node v10.16.0
npm v6.9.0 or above

## Install

Suggestion: use your virtual environment as you with such as conda, virtualenv...etc

do the following:

```script
pip install -r requirements.txt
```

## Usage(@todo)

Activate your virtual environment if you have. Usually the command is `activate virtural_name`

## Development (@todo)

Suggestion: use your virtual environment as you with such as conda, virtualenv...etc

do the following:

```py
npm install
pip install -r requirements.txt
```

## Coding Style

In general, we follow PEP8 Python coding style and Google pyguide
However, if PEP-8 and Google pyguide has conflict style, PEP8 take place.

Some special rule:

1. max-line-length: 100

Reference:

1. https://www.python.org/dev/peps/pep-0008/
2. http://google.github.io/styleguide/pyguide.html

## Project Structure

    .
    DBImport/  
    │  
    ├── bin/  
    │  
    ├── docs/  
    │   └── docs.md  
    │  
    ├── DBImport/  
    │   ├── __init__.py  
    │   ├── runner.py  
    │   └── DBImport/  
    │       ├── __init__.py  
    │       ├── helpers.py  
    │       └── DBImport.py  
    │  
    ├── data/  
    │   └── input.json  
    │  
    ├── scripts/  
    │   ├── pre-commit.sh  
    │   └── pre-push.sh  
    ├── tests/  
    │   ├── 00_empty_test.py  
    │   └── DBImport  
    │       ├── helpers_tests.py  
    │       └── DBImport_tests.py 
    │  
    ├── .gittattributes
    ├── .gitignore
    ├── package.json
    ├── pylintrc
    ├── requirements.txt
    ├── setup.cfg  
    ├── LICENSE  
    └── README.md  

## Git Commit message

In general, we use "Semantic Commit Messages"

Reference:

1. https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716
2. https://github.com/joelparkerhenderson/git_commit_message#begin-with-a-short-summary-line
