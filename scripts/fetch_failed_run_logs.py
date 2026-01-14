#!/usr/bin/env python3
import subprocess, json, os
from pathlib import Path

BRANCH = 'feature/axiom-validation-market-backtesting'
OUTDIR = Path('gh_logs')
OUTDIR.mkdir(exist_ok=True)

# List runs
cmd = ['gh', 'run', 'list', '--branch', BRANCH, '--limit', '50', '--json', 'databaseId,conclusion,workflowName,status']
proc = subprocess.run(cmd, capture_output=True, text=True)
if proc.returncode != 0:
    print('Error listing runs:', proc.stderr)
    raise SystemExit(1)
runs = json.loads(proc.stdout)
failed_runs = [r for r in runs if r.get('conclusion') not in (None, 'success')]
print(f'Found {len(failed_runs)} failed runs')

for r in failed_runs:
    rid = r['databaseId']
    wf = r.get('workflowName', 'unknown').replace(' ', '_')
    run_dir = OUTDIR / f'run_{rid}_{wf}'
    run_dir.mkdir(parents=True, exist_ok=True)
    # get jobs
    p2 = subprocess.run(['gh','run','view',str(rid),'--json','jobs'], capture_output=True, text=True)
    if p2.returncode != 0:
        print(rid, 'Unable to get jobs:', p2.stderr)
        continue
    jobs = json.loads(p2.stdout).get('jobs', [])
    print(f'Run {rid} has {len(jobs)} jobs')
    for job in jobs:
        jid = job['id']
        jname = job.get('name','job').replace('/', '_').replace(' ','_')
        out = run_dir / f'job_{jid}_{jname}.log'
        # Fetch job log
        p3 = subprocess.run(['gh','run','view',str(rid),'--job',str(jid),'--log'], capture_output=True, text=True)
        if p3.returncode != 0:
            print(rid, jid, 'error fetching log:', p3.stderr[:300])
            continue
        if not p3.stdout:
            print(rid, jid, 'no log content')
            continue
        with open(out, 'w', encoding='utf-8') as fh:
            fh.write(p3.stdout)
        print('Saved', out)

# Summarize errors
errors = []
for run_dir in OUTDIR.glob('run_*'):
    for logfile in run_dir.glob('*.log'):
        content = logfile.read_text(encoding='utf-8')
        # find lines with ERROR, failed, Traceback
        for line in content.splitlines():
            if 'ERROR' in line or 'Traceback' in line or 'failed' in line.lower():
                errors.append((logfile, line.strip()))

print('\nSummary of error snippets (first 50):')
for f, l in errors[:50]:
    print(f'{f.name}: {l}')

print('\nSaved logs to', OUTDIR)
print('Done')
