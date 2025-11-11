import sqlite3
import shutil
from datetime import datetime
from pathlib import Path
import argparse
from typing import Union, Optional


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


_THIS_DIR = Path(__file__).resolve().parent
DEFAULT_DB = _THIS_DIR / "database.db"
DEFAULT_BACKUPS_DIR = _THIS_DIR / "backups"


def crear_respaldo(db_path: Union[str, Path] = DEFAULT_DB,
                   backups_dir: Union[str, Path] = DEFAULT_BACKUPS_DIR) -> Path:
    db_path = Path(db_path)
    backups_dir = Path(backups_dir)
    backups_dir.mkdir(parents=True, exist_ok=True)

    if not db_path.exists():
        raise FileNotFoundError(f"La base de datos no existe: {db_path}")

    ts = _timestamp()
    backup_name = f"{db_path.stem}_{ts}{db_path.suffix or '.db'}"
    backup_path = backups_dir / backup_name

    src = sqlite3.connect(str(db_path))
    dst = sqlite3.connect(str(backup_path))
    try:
        with dst:
            src.backup(dst)
    finally:
        dst.close()
        src.close()

    return backup_path


def restaurar_respaldo(backup_file: Union[str, Path],
                       db_path: Union[str, Path] = DEFAULT_DB,
                       backups_dir: Optional[Union[str, Path]] = DEFAULT_BACKUPS_DIR) -> Optional[Path]:
    backup_file = Path(backup_file)
    db_path = Path(db_path)
    backups_dir = None if backups_dir is None else Path(backups_dir)
    if not backup_file.exists():
        raise FileNotFoundError(f"El archivo de respaldo no existe: {backup_file}")
    safety_copy = None
    if backups_dir is not None:
        backups_dir.mkdir(parents=True, exist_ok=True)
        ts = _timestamp()
        safety_name = f"{db_path.stem}_pre_restore_{ts}{db_path.suffix or '.db'}"
        safety_copy = backups_dir / safety_name
        if db_path.exists():
            shutil.copy2(db_path, safety_copy)
        else:
            safety_copy = None
    src = sqlite3.connect(str(backup_file))
    dst = sqlite3.connect(str(db_path))
    try:
        with dst:
            src.backup(dst)
    finally:
        dst.close()
        src.close()
    return safety_copy
def _main():
    parser = argparse.ArgumentParser(description="Crear y restaurar respaldos SQLite (proyecto-final-verde)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create", help="Crear un respaldo")
    p_create.add_argument("--db", "-d", default=str(DEFAULT_DB),
                          help=f"Ruta a la base de datos (default: {DEFAULT_DB})")
    p_create.add_argument("--out", "-o", default=str(DEFAULT_BACKUPS_DIR), help=f"