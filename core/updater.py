# core/updater.py
import os
import subprocess

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def check_and_update():
    """Performs a git pull. Returns True if update happened."""
    try:
        # ensure we're in project dir
        os.chdir(PROJECT_DIR)
        # fetch and pull
        res = subprocess.run(['git', 'pull'], capture_output=True, text=True)
        out = res.stdout + res.stderr
        print('[Updater]', out)
        if 'Already up to date' in out:
            return False
        else:
            return True
    except Exception as e:
        print('[Updater] Update failed:', e)
        return False