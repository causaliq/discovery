param()

# Prefer a local venv (venv39). If it exists, activate it in the current shell
$venv = Join-Path $PSScriptroot '..\venv39'
$py39sys = 'C:\dev\Python3.9.13\python.exe'

if (Test-Path (Join-Path $venv 'Scripts\Activate.ps1')) {
    Write-Host "Activating venv39 at $venv"
    & (Join-Path $venv 'Scripts\Activate.ps1')
    function global:prompt { "py39> " }

    # Update VSCode to use the venv39 interpreter for new terminals
    $settings = Join-Path $PSScriptroot '..\.vscode\settings.json'
    if (Test-Path $settings) {
        $pattern = '"python.defaultInterpreterPath"\s*:\s*".*?"'
        $venvpython = (Join-Path $venv 'Scripts\python.exe')
        $replacement = '"python.defaultInterpreterPath": "' + $venvpython + '"'
        (Get-Content $settings -Raw) -replace $pattern, $replacement | Set-Content $settings
        Write-Host "Updated VSCode to use $venvpython"
    }
    Write-Host "venv39 activated in this shell"

} elseif (Test-Path $py39sys) {
    # No local venv; fall back to setting workspace to the system Python 3.9
    $settings = Join-Path $PSScriptroot '..\.vscode\settings.json'
    if (Test-Path $settings) {
        $pattern = '"python.defaultInterpreterPath"\s*:\s*".*?"'
        $replacement = '"python.defaultInterpreterPath": "' + $py39sys + '"'
        (Get-Content $settings -Raw) -replace $pattern, $replacement | Set-Content $settings
        Write-Host "Updated VSCode to use $py39sys"
    }
    function global:prompt { "py39> " }
    Write-Host "No venv39 found; workspace set to system Python3.9 at $py39sys"

} else {
    Write-Host "Python 3.9 not found at $py39sys and no venv39 present. Edit this script to set the correct path."
}
