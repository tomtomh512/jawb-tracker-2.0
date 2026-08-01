import os
import subprocess
import glob
from datetime import datetime, timedelta
from database import get_app_db_url

BACKUP_DIR = os.getenv("BACKUP_DIR", "backups")
BACKUP_MAX_AGE = timedelta(days=1)
BACKUP_RETENTION = 7  # keep the last N backups

def _ensure_backup_dir():
    os.makedirs(BACKUP_DIR, exist_ok=True)

def _get_backups():
    _ensure_backup_dir()
    return sorted(glob.glob(os.path.join(BACKUP_DIR, "backup_*.dump")))

def _latest_backup():
    backups = _get_backups()
    return backups[-1] if backups else None

def _needs_backup():
    latest = _latest_backup()
    if latest is None:
        return True
    mtime = datetime.fromtimestamp(os.path.getmtime(latest))
    return datetime.now() - mtime > BACKUP_MAX_AGE

def _prune_old_backups():
    backups = _get_backups()
    for old in backups[: len(backups) - BACKUP_RETENTION]:
        os.remove(old)

def create_backup() -> str:
    _ensure_backup_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(BACKUP_DIR, f"backup_{timestamp}.dump")
    result = subprocess.run(
        ["pg_dump", "-Fc", "-f", filepath, get_app_db_url()],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pg_dump failed: {result.stderr}")
    _prune_old_backups()
    return filepath

def run_backup_if_needed():
    if _needs_backup():
        try:
            path = create_backup()
            print(f"[backup] created new backup at {path}")
        except Exception as e:
            print(f"[backup] backup failed: {e}")
    else:
        print(f"[backup] latest backup ({_latest_backup()}) is recent, skipping")

def restore_backup(filepath: str | None = None):
    filepath = filepath or _latest_backup()
    if filepath is None:
        raise RuntimeError("No backup file found to restore from")
    result = subprocess.run(
        ["pg_restore", "--clean", "--if-exists", "-d", get_app_db_url(), filepath],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pg_restore failed: {result.stderr}")
    print(f"[backup] restored from {filepath}")