# Rerun failed GH Actions checks for PR #1
# Requires gh CLI and authentication
gh run list --branch feature/axiom-validation-market-backtesting --limit 50 | Select-String 'workflow\|failed' -Context 0,1
# List runs with status 'failure' and rerun them
$failed = gh run list --branch feature/axiom-validation-market-backtesting --limit 50 --json databaseId,status,conclusion,workflowName | ConvertFrom-Json | Where-Object { $_.conclusion -eq 'failure' -or $_.conclusion -eq 'cancelled'}
if ($failed.Count -eq 0) {
    Write-Host 'No failed runs detected.'
    exit 0
}
foreach ($run in $failed) {
    Write-Host "Re-running run id: $($run.databaseId) (workflow: $($run.workflowName))"
    gh run rerun $run.databaseId
}
