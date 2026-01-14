#!/usr/bin/env python3
"""
Monitor GH Actions runs for a branch, wait for completion, and download logs for failures.
Usage: python scripts/monitor_gh_runs.py --branch feature/axiom-validation-market-backtesting --timeout 900 --poll 10
"""
import argparse
import json
import subprocess
import time
from pathlib import Path


def run_cmd(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{proc.stderr}")
    return proc.stdout


def list_runs(branch, limit=50):
    cmd = [
        'gh', 'run', 'list',
        '--branch', branch,
        '--limit', str(limit),
        '--json', 'databaseId,status,conclusion,workflowName,event,headBranch',
    ]
    out = run_cmd(cmd)
    return json.loads(out)


def tail_runs_status(branch):
    runs = list_runs(branch, limit=100)
    return runs


def download_log(run_id, dest):
    Path(dest).parent.mkdir(parents=True, exist_ok=True)
    with open(dest, 'wb') as f:
        proc = subprocess.run(['gh', 'run', 'view', str(run_id), '--log'], stdout=subprocess.PIPE)
        f.write(proc.stdout)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--branch', required=False, default='feature/axiom-validation-market-backtesting')
    p.add_argument('--poll', type=int, default=15, help='seconds between polls')
    p.add_argument('--timeout', type=int, default=900, help='seconds to wait before timing out')
    p.add_argument('--run-id', help='optional: only monitor this run id')
    p.add_argument('--outdir', default='gh_logs', help='where to store logs')
    args = p.parse_args()
    branch = args.branch

    start = time.time()
    end = start + args.timeout

    print(f"Monitoring GH Actions runs for branch {branch}; poll={args.poll}s; timeout={args.timeout}s")

    while time.time() < end:
        runs = tail_runs_status(branch)
        if args.run_id:
            runs = [r for r in runs if str(r['databaseId']) == str(args.run_id)]
        # If none found, wait and try again
        if not runs:
            print('No runs yet; waiting...')
            time.sleep(args.poll)
            continue

        # Check status
        unfinished = [r for r in runs if r['status'] not in ('completed', 'failure') and r['conclusion'] is None]
        print('Found', len(runs), 'runs (monitoring). Unfinished:', len(unfinished))
        # If none unfinished, all have completed
        if not unfinished:
            # Collect any failing runs
            failed = [r for r in runs if r['conclusion'] not in (None, 'success')]
            if failed:
                print('Found failed runs:', [r['databaseId'] for r in failed])
                for r in failed:
                    rid = r['databaseId']
                    wf = r.get('workflowName', 'unknown')
                    print('Downloading log for', rid, wf)
                    dest = Path(args.outdir) / f"run_{rid}_{wf}.log"
                    try:
                        download_log(rid, dest)
                        print('Saved log to', dest)
                    except Exception as e:
                        print('Failed to download log for', rid, e)
            else:
                print('All runs completed successfully; no failures.')
            return 0

        # Still in progress; show summary and wait
        for r in runs:
            print(f"- {r['databaseId']} {r.get('workflowName','')} status={r['status']} conclusion={r.get('conclusion')}")
        time.sleep(args.poll)

    print('Timed out waiting for runs to complete')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
