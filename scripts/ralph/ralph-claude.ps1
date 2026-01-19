# Ralph for Claude Code - Long-running AI agent loop (PowerShell Edition)
# Usage: .\ralph-claude.ps1 [-MaxIterations 10]

param(
    [int]$MaxIterations = 10
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PrdFile = Join-Path $ScriptDir "prd.json"
$ProgressFile = Join-Path $ScriptDir "progress.txt"
$ArchiveDir = Join-Path $ScriptDir "archive"
$LastBranchFile = Join-Path $ScriptDir ".last-branch"
$PromptFile = Join-Path $ScriptDir "prompt-claude.md"

# Check for claude CLI
$claudeCmd = Get-Command claude -ErrorAction SilentlyContinue
if (-not $claudeCmd) {
    Write-Error "Error: Claude Code CLI is required but not installed."
    Write-Host "Install with: npm install -g @anthropic-ai/claude-code"
    exit 1
}

# Function to read JSON safely
function Get-JsonProperty {
    param([string]$FilePath, [string]$Property)
    try {
        $json = Get-Content $FilePath -Raw | ConvertFrom-Json
        return $json.$Property
    } catch {
        return $null
    }
}

# Archive previous run if branch changed
if ((Test-Path $PrdFile) -and (Test-Path $LastBranchFile)) {
    $CurrentBranch = Get-JsonProperty -FilePath $PrdFile -Property "branchName"
    $LastBranch = Get-Content $LastBranchFile -ErrorAction SilentlyContinue

    if ($CurrentBranch -and $LastBranch -and ($CurrentBranch -ne $LastBranch)) {
        # Archive the previous run
        $Date = Get-Date -Format "yyyy-MM-dd"
        $FolderName = $LastBranch -replace "^ralph/", ""
        $ArchiveFolder = Join-Path $ArchiveDir "$Date-$FolderName"

        Write-Host "Archiving previous run: $LastBranch"
        New-Item -ItemType Directory -Path $ArchiveFolder -Force | Out-Null
        if (Test-Path $PrdFile) { Copy-Item $PrdFile $ArchiveFolder }
        if (Test-Path $ProgressFile) { Copy-Item $ProgressFile $ArchiveFolder }
        Write-Host "   Archived to: $ArchiveFolder"

        # Reset progress file for new run
        @"
# Ralph Progress Log
Started: $(Get-Date)
---
"@ | Set-Content $ProgressFile
    }
}

# Track current branch
if (Test-Path $PrdFile) {
    $CurrentBranch = Get-JsonProperty -FilePath $PrdFile -Property "branchName"
    if ($CurrentBranch) {
        $CurrentBranch | Set-Content $LastBranchFile
    }
}

# Initialize progress file if it doesn't exist
if (-not (Test-Path $ProgressFile)) {
    @"
# Ralph Progress Log
Started: $(Get-Date)
---
"@ | Set-Content $ProgressFile
}

Write-Host ""
Write-Host "Starting Ralph (Claude Code Edition) - Max iterations: $MaxIterations"
Write-Host "Working directory: $(Get-Location)"
Write-Host ""

for ($i = 1; $i -le $MaxIterations; $i++) {
    Write-Host ""
    Write-Host "======================================================="
    Write-Host "  Ralph Iteration $i of $MaxIterations"
    Write-Host "======================================================="

    # Read prompt content
    $PromptContent = Get-Content $PromptFile -Raw

    # Run Claude Code with the ralph prompt
    try {
        $Output = $PromptContent | claude --dangerously-skip-permissions --print 2>&1
        $Output | Write-Host
    } catch {
        Write-Host "Iteration encountered an error: $_"
        $Output = ""
    }

    # Check for completion signal
    if ($Output -match "<promise>COMPLETE</promise>") {
        Write-Host ""
        Write-Host "Ralph completed all tasks!"
        Write-Host "Completed at iteration $i of $MaxIterations"
        exit 0
    }

    Write-Host "Iteration $i complete. Continuing..."
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "Ralph reached max iterations ($MaxIterations) without completing all tasks."
Write-Host "Check $ProgressFile for status."
exit 1
