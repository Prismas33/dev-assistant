<#
.SYNOPSIS
    Initialize documentation structure in a new project.

.DESCRIPTION
    Copies the embedded documentation template to the target project.
    This script should be run from the skill's installation directory.

.PARAMETER ProjectPath
    Path to the project where documentation will be created.
    Default: current directory (.)

.PARAMETER Force
    Overwrite if documentation already exists.

.EXAMPLE
    .\init-project.ps1 -ProjectPath "C:\my-project"
    
.EXAMPLE
    .\init-project.ps1
    # Uses current directory

.NOTES
    The AI agent can also create the structure manually by reading
    the templates/ folder and creating files in the target project.
#>

param(
    [string]$ProjectPath = ".",
    [switch]$Force
)

# Configuration
$DOC_FOLDER = "doc"

# Get script directory (where templates are)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillDir = Split-Path -Parent $ScriptDir
$TEMPLATE_PATH = Join-Path $SkillDir "templates"

# Resolve absolute path
$ProjectPath = Resolve-Path $ProjectPath -ErrorAction SilentlyContinue
if (-not $ProjectPath) {
    Write-Host "Error: Project path not found!" -ForegroundColor Red
    exit 1
}

$DestPath = Join-Path $ProjectPath $DOC_FOLDER

# Check if templates exist
if (-not (Test-Path $TEMPLATE_PATH)) {
    Write-Host "Error: Templates not found at: $TEMPLATE_PATH" -ForegroundColor Red
    Write-Host "   Make sure the skill is properly installed." -ForegroundColor Yellow
    exit 1
}

# Check if doc already exists
if ((Test-Path $DestPath) -and -not $Force) {
    Write-Host "Warning: '$DOC_FOLDER' folder already exists at: $ProjectPath" -ForegroundColor Yellow
    Write-Host "   Use -Force to overwrite." -ForegroundColor Yellow
    exit 0
}

# Copy template
Write-Host "Copying documentation template..." -ForegroundColor Cyan
Write-Host "   From: $TEMPLATE_PATH" -ForegroundColor Gray
Write-Host "   To: $DestPath" -ForegroundColor Gray

try {
    Copy-Item -Path $TEMPLATE_PATH -Destination $DestPath -Recurse -Force
    
    # Rename destination folder from 'templates' to 'doc'
    # Actually Copy-Item with folder creates the content inside, so this should work
    
    Write-Host "Documentation created successfully!" -ForegroundColor Green
    
    # List created structure
    Write-Host "`nCreated structure:" -ForegroundColor Cyan
    Get-ChildItem -Path $DestPath -Recurse -Directory | ForEach-Object {
        $indent = "   " * ($_.FullName.Split('\').Count - $DestPath.Split('\').Count)
        Write-Host "$indent - $($_.Name)/" -ForegroundColor Gray
    }
    
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "   1. Fill doc/MEMORIA.md with project context"
    Write-Host "   2. Create first entry in doc/desenvolvimento/diario.md"
    Write-Host "   3. Adapt code rules if needed"
    
} catch {
    Write-Host "Error copying template: $_" -ForegroundColor Red
    exit 1
}
