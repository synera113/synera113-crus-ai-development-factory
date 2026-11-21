# CRUS Kurulum Kılavuzu

## Gereksinimler

- Windows 11
- Python 3.12 veya üzeri
- Docker Desktop (Docker seçeneği için)

## Yerel demo kurulumu

```powershell
./setup.ps1
./start.ps1
```

Backend adresi: http://127.0.0.1:8000

Swagger dokümantasyonu: http://127.0.0.1:8000/docs

## Docker kurulumu

```powershell
./start.ps1 -Docker
./stop.ps1
```

Durdurma: Yerel HTTP sunucusunda terminalde `Ctrl+C` kullanın; Docker için `./stop.ps1` çalıştırın.

## Demo modu

`.env.example` dosyasındaki `CRUS_MODE=demo` değeri dış AI API anahtarı gerektirmeden yerel demo çalıştırır.
