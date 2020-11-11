# Update File

Automatically update a file based a script.

Currently we only support Python scripts. If asked, support for other languages can be added.

## How to use

Install this GitHub action by creating a file in your repo at `.github/workflows/update-file.yml`.

A minimal example could be:

```YAML
name: Update File

on:
  push:
  schedule:
  - cron: "0 0 * * *"

jobs:
  update-file:
    runs-on: ubuntu-latest
    steps:
        - uses: actions/checkout@v2
      - uses: kludex/update-file
        with:
          script_file: update_script.py
          update_file: README.md
```
In this minimal example, you need:
- `script_file`: script location
- `update_file`: file to update

And it will run on `push` and on `schedule` (`cron: "0 0 * * *"`), so each day at midnight the script `update_script.py` will update the `README.md`.

## License

This project is licensed under the terms of the MIT license.
