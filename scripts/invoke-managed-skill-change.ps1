<#
.SYNOPSIS
    Runs one previously reviewed skill-management command and reconciles the registry.

.DESCRIPTION
    This wrapper does not choose, download, or approve a skill. Supply the exact
    command already reviewed for this change. Arguments are not logged, because
    installer arguments may contain sensitive values. A failed change never
    advances the catalog; a failed reconciliation returns an error for repair.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateSet('install', 'update', 'remove')]
    [string]$Event,

    [Parameter(Mandatory)]
    [string]$Executable,

    [string[]]$ChangeArguments = @(),

    [Parameter(Mandatory)]
    [switch]$Reviewed,

    [string]$PythonPath = 'python',
    [string]$CodexHome = 'C:\Users\ventu\.codex',
    [string]$AgentsHome = 'C:\Users\ventu\.agents',
    [string]$Utilities = 'E:\utilitarios',
    [string]$ProjectRoot = 'E:\projetos-vs',
    [switch]$NoPlugins
)

$ErrorActionPreference = 'Stop'
if (-not $Reviewed) { throw 'A revisão da origem, scripts e revisão exata deve preceder esta operação.' }

$resolvedCommand = Get-Command -Name $Executable -ErrorAction Stop
$registryScript = Join-Path $PSScriptRoot 'skills_registry.py'
if (-not (Test-Path -LiteralPath $registryScript -PathType Leaf)) {
    throw "Registry script missing: $registryScript"
}

& $resolvedCommand.Source @ChangeArguments
$changeExit = $LASTEXITCODE
if ($changeExit -ne 0) {
    throw "A operação de skill falhou com exit code $changeExit; catálogo não alterado."
}

$registryArguments = @(
    $registryScript, '--codex-home', $CodexHome, '--agents-home', $AgentsHome,
    '--utilities', $Utilities, '--project-root', $ProjectRoot,
    'reconcile', '--event', $Event
)
if ($NoPlugins) { $registryArguments += '--no-plugins' }

& $PythonPath @registryArguments
if ($LASTEXITCODE -ne 0) {
    throw 'A operação da skill terminou, mas a reconciliação falhou; reparar o catálogo antes de reportar conclusão.'
}

Write-Output 'OK: operação revista e catálogo sincronizado.'
