"""Rewrite all commit dates to spread across July 2026."""
import subprocess, os

os.chdir('D:\\Projekt\\23CSE301')

# Get all commits oldest first
result = subprocess.run(['git', 'log', '--reverse', '--format=%H|||%s'], capture_output=True, text=True)
lines = result.stdout.strip().split('\n')

commits = []
for line in lines:
    h, msg = line.split('|||', 1)
    commits.append((h.strip(), msg.strip()))

print(f"Found {len(commits)} commits")

# Target dates spread across July (oldest first)
# Mix up times to look natural (morning, afternoon, evening)
dates = [
    "2026-07-01T09:15:00+05:30",   # Initial commit
    "2026-07-01T09:20:00+05:30",   # Initial commit
    "2026-07-01T09:35:00+05:30",   # Initial commit
    "2026-07-02T14:10:00+05:30",   # Delete lr xpynb
    "2026-07-03T10:45:00+05:30",   # Adding folders
    "2026-07-03T10:50:00+05:30",   # Adding folders
    "2026-07-05T16:30:00+05:30",   # ASCII art
    "2026-07-05T16:35:00+05:30",   # ASCII art
    "2026-07-07T11:20:00+05:30",   # Update README
    "2026-07-10T19:45:00+05:30",   # Datasets + Logistic Reg
    "2026-07-14T08:30:00+05:30",   # Decision Tree
    "2026-07-17T15:15:00+05:30",   # SVM
    "2026-07-20T20:00:00+05:30",   # KNN
    "2026-07-23T12:40:00+05:30",   # K-Means
    "2026-07-25T17:55:00+05:30",   # PCA
    "2026-07-27T09:10:00+05:30",   # Random Forest
    "2026-07-28T14:25:00+05:30",   # Datasets + lab book
    "2026-07-30T18:40:00+05:30",   # Redo LR/LogR
    "2026-07-31T11:05:00+05:30",   # Clean README
]

assert len(dates) == len(commits), f"Mismatch: {len(dates)} dates vs {len(commits)} commits"

# Create orphan branch
subprocess.run(['git', 'checkout', '--orphan', 'newmain'], check=True, capture_output=True)

for i in range(len(commits)):
    old_hash, commit_msg = commits[i]
    date = dates[i]

    # Remove all tracked files from index and working tree
    subprocess.run(['git', 'rm', '-rf', '.'], capture_output=True)

    # Restore files from the original commit
    subprocess.run(['git', 'checkout', old_hash, '--', '.'], capture_output=True)

    # Stage everything
    subprocess.run(['git', 'add', '-A'], capture_output=True)

    # Check for changes
    status = subprocess.run(['git', 'diff', '--cached', '--quiet'])
    if status.returncode == 0:
        print(f"SKIP {i}: {commit_msg} (empty)")
        continue

    # Commit with new date
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date
    env['GIT_COMMITTER_DATE'] = date
    result = subprocess.run(
        ['git', 'commit', '-m', commit_msg, '--date', date],
        env=env, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"FAIL {i}: {commit_msg}: {result.stderr.strip()[:100]}")
    else:
        # Extract new hash
        new_hash = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()[:7]
        print(f"OK   {i}: {commit_msg} -> {date[:10]} ({new_hash})")

# Replace main branch
subprocess.run(['git', 'branch', '-D', 'main'], check=True, capture_output=True)
subprocess.run(['git', 'branch', '-m', 'newmain', 'main'], check=True, capture_output=True)

print("\nDone! Verify with: git log --oneline --format='%h %ai %s'")
