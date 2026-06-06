$projects = @(
    [pscustomobject]@{
        Name = "hermes-geral"
        Description = "Hermes Geral / Desenvolvedor"
        GitHub = "https://github.com/haniellevi/hermes-geral-raniellevi"
        LocalPath = "C:\Users\hanie\OneDrive\Documentos\WORKSPACE\Projetos Locais\HERMES-GERAL"
        VpsPath = "/opt/hermes-geral"
        Branch = "main"
    },
    [pscustomobject]@{
        Name = "hermes-pastoral"
        Description = "Hermes Gestao Pastoral / Igreja Filadelfia"
        GitHub = "https://github.com/haniellevi/gestor-pastoral-agente-hermes"
        LocalPath = "C:\Users\hanie\OneDrive\Documentos\WORKSPACE\Projetos Locais\Gestao Pastoral - Pr Raniel Levi\HERMES-LOCAL"
        VpsPath = "/opt/gestor-pastoral-agente-hermes/HERMES-LOCAL"
        Branch = "feature/instalacao-hermes"
    }
)

$projects | Format-Table -AutoSize
