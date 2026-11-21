if (Get-Command docker -ErrorAction SilentlyContinue) {
    docker compose down
}
