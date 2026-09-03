$ErrorActionPreference = "Stop"

$repositoryPath = $PSScriptRoot
$intervalSeconds = 30

Set-Location $repositoryPath

while ($true) {
    try {
        $changes = git status --porcelain
        $pendingPush = git rev-list --count '@{u}..HEAD' 2>$null

        if ($changes) {
            git add --all

            $commitMessage = "Auto-commit: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            git commit -m $commitMessage
        }

        if ($changes -or [int]$pendingPush -gt 0) {
            git push

            Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Commit and push complete"
        }
        else {
            Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] No changes"
        }
    }
    catch {
        Write-Warning "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Commit/push failed: $($_.Exception.Message)"
    }

    Start-Sleep -Seconds $intervalSeconds
}