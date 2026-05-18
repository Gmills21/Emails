# AGENTS.md

## Cursor Cloud specific instructions

This is a **data-only repository** containing CSV exports of email inboxes from Microsoft Outlook. There is no application code, build system, package manager, or services to run.

### Repository contents

- `Inbox.CSV`, `Inbox2.CSV`, `Inbox3.CSV`, `Inbox4.CSV` — email data exports (UTF-8 with BOM, 19 columns, ~2,791 rows total)
- `README.md` — minimal project description

### Working with the data

- CSV files use UTF-8-BOM encoding; open with `encoding='utf-8-sig'` in Python.
- Python 3 with the built-in `csv` module is sufficient for reading/processing. No external packages are required.
- There are no lint, test, or build steps for this repository.

### Development environment

No dependencies need to be installed. The VM's default Python 3 installation is sufficient for any data exploration tasks.
