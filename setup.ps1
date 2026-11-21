param($ErrorAction = "Stop")

Write-Host "CRUS AI Development Factory - setup" -ForegroundColor Cyan

if (-not (Get-Command py -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python bulunamadı. Python 3.12 yükleyin." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".venv")) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3.12 -m venv .venv
    } else {
        python -m venv .venv
    }
}

& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt

if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
}

Write-Host "Kurulum tamamlandı." -ForegroundColor Green
