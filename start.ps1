param([switch]$Docker)

if ($Docker) {
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Host "Docker bulunamadı." -ForegroundColor Red
        exit 1
    }
    docker compose up -d --build
    Write-Host "CRUS backend: http://localhost:8000" -ForegroundColor Green
    Write-Host "API docs: http://localhost:8000/docs" -ForegroundColor Cyan
    exit 0
}

if (-not (Test-Path ".venv")) {
    Write-Host "Önce ./setup.ps1 çalıştırın." -ForegroundColor Red
    exit 1
}

& .\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
