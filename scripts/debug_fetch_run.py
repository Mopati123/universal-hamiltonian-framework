import subprocess, json, sys
rid = sys.argv[1] if len(sys.argv)>1 else '20167234732'
print('Fetching run', rid)
cmd = ['gh','run','view',rid,'--repo','Mopati123/universal-hamiltonian-framework','--json','jobs']
proc = subprocess.run(cmd,capture_output=True,text=True)
print('rc', proc.returncode)
if proc.stderr:
    print('stderr', proc.stderr[:400])
    sys.exit(1)
jobs = json.loads(proc.stdout).get('jobs', [])
print('Jobs:', len(jobs))
for j in jobs:
    print('Job:', j['id'], j['name'], j.get('status'), j.get('conclusion'))
    jobid=str(j['id'])
    p2=subprocess.run(['gh','run','view',rid,'--job',jobid,'--repo','Mopati123/universal-hamiltonian-framework','--log'],capture_output=True,text=True)
    print('rc2', p2.returncode, 'len', len(p2.stdout))
    if p2.stdout:
        print(p2.stdout.splitlines()[:20])
    else:
        print('No stdout for job', jobid)

print('done')
