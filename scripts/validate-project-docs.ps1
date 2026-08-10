<#
.SYNOPSIS
    Validates the required dev-assistant documentation structure.
#>

[CmdletBinding()]
param(
    [string]$ProjectPath = ".",
    [switch]$StructureOnly
)

$ErrorActionPreference = "Stop"
$resolvedProject = Resolve-Path -LiteralPath $ProjectPath -ErrorAction SilentlyContinue
if (-not $resolvedProject) {
    throw "Project path not found: $ProjectPath"
}

$required = @(
    "doc/MEMORIA.md",
    "doc/CHANGELOG.md",
    "doc/componentes/README.md",
    "doc/desenvolvimento/README.md",
    "doc/desenvolvimento/diario.md",
    "doc/desenvolvimento/regras-arquitetura-modular.md",
    "doc/desenvolvimento/regras-codigo.md",
    "doc/desenvolvimento/regras-documentacao.md",
    "doc/desenvolvimento/regras-layout.md",
    "doc/desenvolvimento/regras-seguranca.md",
    "doc/design/design-system.md",
    "doc/negocio/mercado.md",
    "doc/negocio/modelo-negocio.md",
    "doc/negocio/visao-geral.md",
    "doc/planeamento/riscos.md",
    "doc/planeamento/roadmap.md",
    "doc/produto/features-mvp.md",
    "doc/produto/fluxo-produto.md",
    "doc/produto/kpis.md",
    "doc/tecnico/arquitetura.md",
    "doc/tecnico/integracoes.md",
    "doc/tecnico/variaveis-ambiente.md"
)

$missing = [System.Collections.Generic.List[string]]::new()
$empty = [System.Collections.Generic.List[string]]::new()
$placeholders = [System.Collections.Generic.List[string]]::new()
$placeholderPattern = '(\[NOME_PROJETO\]|\[Nome[^\]]*\]|\[Feature[^\]]*\]|\[Servico[^\]]*\]|\[Data[^\]]*\]|\[URL[^\]]*\]|X\.X)'

foreach ($relativePath in $required) {
    $path = Join-Path $resolvedProject.Path $relativePath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        $missing.Add($relativePath)
        continue
    }

    $content = Get-Content -Raw -LiteralPath $path
    if ([string]::IsNullOrWhiteSpace($content)) {
        $empty.Add($relativePath)
        continue
    }

    if (-not $StructureOnly -and $content -match $placeholderPattern) {
        $placeholders.Add($relativePath)
    }
}

if ($missing.Count -gt 0) {
    Write-Output "Missing files:"
    $missing | ForEach-Object { Write-Output "  - $_" }
}

if ($empty.Count -gt 0) {
    Write-Output "Empty files:"
    $empty | ForEach-Object { Write-Output "  - $_" }
}

if ($placeholders.Count -gt 0) {
    Write-Output "Unresolved template placeholders:"
    $placeholders | ForEach-Object { Write-Output "  - $_" }
}

if ($missing.Count -gt 0 -or $empty.Count -gt 0 -or $placeholders.Count -gt 0) {
    exit 1
}

Write-Output "OK: project documentation is complete."
