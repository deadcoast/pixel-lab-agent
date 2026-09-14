$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$pixlPython = 'C:/Users/ryanf/github/pixel-lab-docsuite/.venv/Scripts/python.exe'
$pixlRunner = Join-Path $projectRoot '.agents/skills/pixl-kit/scripts/pixl.py'
$pixlState = Join-Path $projectRoot '.pixl/state.px'
& $pixlPython $pixlRunner family $pixlState --root $projectRoot
& $pixlPython $pixlRunner workflow $pixlState --root $projectRoot
& $pixlPython $pixlRunner jobs $pixlState --root $projectRoot
