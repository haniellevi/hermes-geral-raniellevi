param(
    [string]$ProjectRoot = "C:\Users\hanie\OneDrive\Documentos\WORKSPACE\Projetos Locais\HERMES-GERAL"
)

$ErrorActionPreference = "Stop"

Set-Location -LiteralPath $ProjectRoot
$env:HERMES_CODEX_LOCAL_ENABLED = "1"

python -m app.telegram_bot
