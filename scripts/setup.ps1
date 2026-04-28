$ErrorActionPreference = "Stop"

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw "npm is required but was not found on PATH."
}

if (-not (Test-Path "backend/.venv/Scripts/python.exe")) {
    throw "Backend virtual environment not found. Run 'npm run setup' first."
}

$frontendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    npm --prefix frontend run dev 2>&1
}

$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    & "backend/.venv/Scripts/python.exe" "backend/app.py" 2>&1
}

Write-Host "Frontend and backend are starting..."
Write-Host "Frontend: http://localhost:5173"
Write-Host "Backend:  http://localhost:5000"
Write-Host "Press Ctrl+C to stop both."

try {
    while ($true) {
        Receive-Job $frontendJob -Keep -ErrorAction SilentlyContinue
        Receive-Job $backendJob -Keep -ErrorAction SilentlyContinue

        if ($frontendJob.State -match "Failed|Completed|Stopped") {
            throw "Frontend process exited."
        }

        if ($backendJob.State -match "Failed|Completed|Stopped") {
            throw "Backend process exited."
        }

        Start-Sleep -Milliseconds 500
    }
}
finally {
    Stop-Job -Job $frontendJob, $backendJob -ErrorAction SilentlyContinue
    Remove-Job -Job $frontendJob, $backendJob -Force -ErrorAction SilentlyContinue
}