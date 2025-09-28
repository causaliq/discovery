param()

# Activate and set workspace to venv311
$venv = Join-Path $PSScriptroot '..\venv311'
$venvpython = Join-Path $venv 'Scripts\python.exe'

if (Test-Path (Join-Path $venv 'Scripts\Activate.ps1')) {
    Write-Host "Activating venv311 at $venv"
    & (Join-Path $venv 'Scripts\Activate.ps1')
    function global:prompt { "py311> " }

    # Update VSCode to use the venv311 interpreter for new terminals
    $settings = Join-Path $PSScriptroot '..\.vscode\settings.json'
    if (Test-Path $settings) {
        $pattern = '"python.defaultInterpreterPath"\s*:\s*".*?"'
        $replacement = '"python.defaultInterpreterPath": "' + $venvpython + '"'
        (Get-Content $settings -Raw) -replace $pattern, $replacement | Set-Content $settings
        Write-Host "Updated VSCode to use $venvpython"
    }
    Write-Host "venv311 activated in this shell"
} else {
    Write-Host "venv311 not found at $venv"
}
