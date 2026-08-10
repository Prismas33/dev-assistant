<#
.SYNOPSIS
    Creates missing project documentation from the bundled templates.

.DESCRIPTION
    Merge-safe by default: existing project files are preserved byte-for-byte.
    Use -Overwrite only when the user explicitly authorized replacement.
#>

[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$ProjectPath = ".",
    [switch]$Overwrite
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillDir = Split-Path -Parent $scriptDir
$templatePath = Join-Path $skillDir "templates"

if (-not (Test-Path -LiteralPath $templatePath -PathType Container)) {
    throw "Templates not found: $templatePath"
}

$resolvedProject = Resolve-Path -LiteralPath $ProjectPath -ErrorAction SilentlyContinue
if (-not $resolvedProject) {
    throw "Project path not found: $ProjectPath"
}

$destinationRoot = Join-Path $resolvedProject.Path "doc"
$created = [System.Collections.Generic.List[string]]::new()
$updated = [System.Collections.Generic.List[string]]::new()
$preserved = [System.Collections.Generic.List[string]]::new()

Get-ChildItem -LiteralPath $templatePath -Recurse -File | ForEach-Object {
    $relativePath = $_.FullName.Substring($templatePath.Length).TrimStart('\', '/')
    $destination = Join-Path $destinationRoot $relativePath
    $exists = Test-Path -LiteralPath $destination -PathType Leaf

    if ($exists -and -not $Overwrite) {
        $preserved.Add($relativePath)
        return
    }

    $parent = Split-Path -Parent $destination
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    $action = if ($exists) { "Overwrite documentation file" } else { "Create documentation file" }
    if ($PSCmdlet.ShouldProcess($destination, $action)) {
        Copy-Item -LiteralPath $_.FullName -Destination $destination -Force
        if ($exists) { $updated.Add($relativePath) } else { $created.Add($relativePath) }
    }
}

Write-Output "Documentation setup complete."
Write-Output "Created: $($created.Count)"
$created | ForEach-Object { Write-Output "  + $_" }
Write-Output "Updated: $($updated.Count)"
$updated | ForEach-Object { Write-Output "  ~ $_" }
Write-Output "Preserved: $($preserved.Count)"
$preserved | ForEach-Object { Write-Output "  = $_" }

if ($preserved.Count -gt 0 -and -not $Overwrite) {
    Write-Output "Existing files were preserved. Review and update them explicitly when required."
}
