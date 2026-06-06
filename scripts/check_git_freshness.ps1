param(
    [string]$Path = "."
)

$ErrorActionPreference = "Stop"

Set-Location -LiteralPath $Path

if (-not (Test-Path ".git")) {
    throw "Nao e um repositorio Git: $Path"
}

$branch = git branch --show-current
if (-not $branch) {
    throw "Nao foi possivel identificar a branch atual."
}

git fetch --all --prune | Out-Host

$upstream = git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>$null
if (-not $upstream) {
    Write-Output "branch=$branch"
    Write-Output "upstream=NAO_CONFIGURADO"
    Write-Output "status=sem_upstream"
    git status --short
    exit 0
}

$local = git rev-parse HEAD
$remote = git rev-parse "@{u}"
$base = git merge-base HEAD "@{u}"

Write-Output "branch=$branch"
Write-Output "upstream=$upstream"
Write-Output "local=$local"
Write-Output "remote=$remote"
Write-Output "base=$base"

if ($local -eq $remote) {
    Write-Output "status=sincronizado"
} elseif ($local -eq $base) {
    Write-Output "status=remoto_na_frente"
    Write-Output "acao_recomendada=git pull --ff-only"
} elseif ($remote -eq $base) {
    Write-Output "status=local_na_frente"
    Write-Output "acao_recomendada=git push"
} else {
    Write-Output "status=divergente"
    Write-Output "acao_recomendada=parar_e_decidir"
}

Write-Output "working_tree="
git status --short
