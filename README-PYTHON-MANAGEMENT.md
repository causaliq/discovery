This repo includes small helper scripts to switch the VSCode workspace Python interpreter and open shells pre-configured for the chosen interpreter.

Files added (scripts/)
- use-py311.bat  : Activate the local venv311 (Windows cmd)
- use-py311.ps1  : Activate the local venv311 (PowerShell)
- use-py39.bat   : Update VSCode to point to a Python 3.9 interpreter and set a P39 prompt (cmd)
- use-py39.ps1   : Same for PowerShell (edit to set the correct 3.9 path)

Design
- Default VSCode interpreter is set to the repository-local `venv311` in `.vscode/settings.json`.
- To switch to Python 3.9, edit `scripts/use-py39.*` to point to your Python 3.9 executable and run the script. It will update VSCode's `python.defaultInterpreterPath` setting.

Usage examples
- From cmd.exe to switch to 3.11 (activate venv):
  scripts\\use-py311.bat

- From PowerShell to switch to 3.11:
  .\\scripts\\use-py311.ps1

- From cmd.exe to switch VSCode to use a global Python 3.9 (edit path first):
  scripts\\use-py39.bat

- From PowerShell to switch VSCode to Python 3.9:
  .\\scripts\\use-py39.ps1

Note
- The scripts update `.vscode/settings.json` so VSCode will use the chosen interpreter for linting, intellisense, and the built-in terminal if `python.terminal.activateEnvironment` is enabled.
- They do not change your system PATH.
- For exact reproducibility across Python versions, use the generated `venv311-requirements.txt` and create a fresh venv for each Python version.
