$storageDir = "C:\Users\$env:USERNAME\AppData\Roaming\Code\User\globalStorage\local.ltm-dct-assistant"
$pythonExe = "C:\Program Files\Python312\Python.exe"

Remove-Item Env:PYTHONHOME -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONPLATLIBDIR -ErrorAction SilentlyContinue
Remove-Item Env:__PYVENV_LAUNCHER__ -ErrorAction SilentlyContinue

if (!(Test-Path $storageDir)) {
    New-Item -ItemType Directory -Path $storageDir -Force | Out-Null
}

$bundledRuntime = Join-Path $storageDir "bundled-runtime"
$requirementsFile = Join-Path $bundledRuntime "requirements.txt"
$serverFile = Join-Path $bundledRuntime "backend\mcp_server.py"
$venvDir = Join-Path $storageDir "python-env"
$venvPython = Join-Path $venvDir "Scripts\python.exe"

if (!(Test-Path $bundledRuntime)) {
    Write-Error "Missing bundled-runtime folder at $bundledRuntime"
    exit 1
}

if (!(Test-Path $requirementsFile)) {
    Write-Error "Missing requirements.txt at $requirementsFile"
    exit 1
}

if (!(Test-Path $serverFile)) {
    Write-Error "Missing mcp_server.py at $serverFile"
    exit 1
}

if (!(Test-Path $pythonExe)) {
    Write-Error "Python not found at $pythonExe"
    exit 1
}

if (Test-Path $venvDir) {
    Remove-Item $venvDir -Recurse -Force
}

Write-Host "Creating virtual environment..."
& $pythonExe -m venv $venvDir
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to create virtual environment"
    exit 1
}

Write-Host "Upgrading pip..."
& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to upgrade pip"
    exit 1
}

Write-Host "Installing requirements..."
& $venvPython -m pip install -r $requirementsFile
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install requirements"
    exit 1
}

Write-Host "Testing MCP server startup..."
& $venvPython $serverFile
