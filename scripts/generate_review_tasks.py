import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

files = subprocess.check_output(['git', 'ls-files'], cwd=REPO_ROOT).decode().splitlines()

with open(REPO_ROOT / 'REVIEW_TASKS.md', 'w') as f:
    f.write('# File Review Tasks\n\n')
    f.write('Generated list of files to manually review. Check off items as you complete the review.\n\n')
    for file in files:
        f.write(f'- [ ] `{file}`\n')
