import tempfile
import unittest
from pathlib import Path

from src.backup_manager import BackupManager


class BackupManagerIgnoreTests(unittest.TestCase):
    def test_nested_backup_folders_are_not_repacked(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            manager = BackupManager(backup_dir=root / "backups", data_dir=root / "data")

            for folder in ("tutoria_backups", "backups_listas_turmas", "backup_extraido"):
                candidate = root / "data" / folder / "old.json"
                self.assertTrue(manager._deve_ignorar(candidate), folder)

    def test_current_tutoring_data_is_kept(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            manager = BackupManager(backup_dir=root / "backups", data_dir=root / "data")

            candidate = root / "data" / "tutoria_cadastro.json"
            self.assertFalse(manager._deve_ignorar(candidate))

    def test_tutoria_retention_keeps_the_newest_snapshots(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            backup_dir = Path(temporary_dir)
            for index in range(5):
                backup = backup_dir / f"tutoria_backup_2026102{index}_120000_000000.json"
                backup.write_text(str(index), encoding="utf-8")

            BackupManager.limpar_backups_tutoria(backup_dir, limite=3)

            remaining = sorted(path.read_text(encoding="utf-8") for path in backup_dir.glob("*.json"))
            self.assertEqual(remaining, ["2", "3", "4"])


if __name__ == "__main__":
    unittest.main()