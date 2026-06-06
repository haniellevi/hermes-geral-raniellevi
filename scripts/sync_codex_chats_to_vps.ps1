param(
    [string]$ProjectRoot = "C:\Users\hanie\OneDrive\Documentos\WORKSPACE\Projetos Locais\HERMES-GERAL",
    [string]$SshKey = "$env:USERPROFILE\.ssh\id_ed25519_hostinger_hermes",
    [string]$VpsHost = "root@2.25.167.107",
    [string]$RemoteDir = "/opt/hermes-geral/conhecimento/codex_chats",
    [int]$Limit = 30
)

$ErrorActionPreference = "Stop"

Set-Location -LiteralPath $ProjectRoot
python scripts/export_codex_chats.py --limit $Limit --output conhecimento/codex_chats

ssh -i $SshKey -o BatchMode=yes $VpsHost "mkdir -p '$RemoteDir'"
scp -i $SshKey -o BatchMode=yes -r "$ProjectRoot\conhecimento\codex_chats\*" "${VpsHost}:${RemoteDir}/"

ssh -i $SshKey -o BatchMode=yes $VpsHost "find '$RemoteDir' -maxdepth 1 -type f | wc -l"
