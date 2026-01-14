import subprocess
import json

branch = 'feature/axiom-validation-market-backtesting'

cmd = ['gh', 'run', 'list', '--branch', branch, '--limit', '50', '--json', 'databaseId,conclusion,workflowName']
proc = subprocess.run(cmd, capture_output=True, text=True)
if proc.returncode != 0:
    print('Error listing runs:', proc.stderr)
    raise SystemExit(1)

runs = json.loads(proc.stdout)
failed = [r for r in runs if r.get('conclusion') in ('failure', 'cancelled')]
if not failed:
    print('No failed runs found.')
else:
    for r in failed:
        print(f"Rerunning run {r['databaseId']} (workflow: {r['workflowName']})")
        rerun = subprocess.run(['gh', 'run', 'rerun', str(r['databaseId'])])
        if rerun.returncode != 0:
            print('Failed to rerun', r['databaseId'])

print('Done')
