from pathlib import Path
import zipfile
import tarfile
import gzip
import shutil
import tempfile

from A_03_HANDLERS.base_handler import BaseHandler


class ArchiveHandler(BaseHandler):

    supported_extensions = [
        ".zip",
        ".tar",
        ".tgz",
        ".gz",
    ]

    def can_handle(self, path: Path) -> bool:
        name = path.name.lower()
        suffix = path.suffix.lower()
        return (
            suffix in self.supported_extensions
            or name.endswith(".tar.gz")
        )

    def extract(self, path: Path):

        path = Path(path)
        name = path.name.lower()

        try:
            members = []
            extracted_preview = []

            with tempfile.TemporaryDirectory(prefix="butler_archive_") as tmp:
                tmp_dir = Path(tmp)

                if name.endswith(".zip"):
                    with zipfile.ZipFile(path, "r") as zf:
                        members = zf.namelist()
                        self._safe_extract_zip(zf, tmp_dir)

                elif name.endswith(".tar") or name.endswith(".tar.gz") or name.endswith(".tgz"):
                    mode = "r:gz" if (name.endswith(".tar.gz") or name.endswith(".tgz")) else "r"
                    with tarfile.open(path, mode) as tf:
                        members = tf.getnames()
                        self._safe_extract_tar(tf, tmp_dir)

                elif name.endswith(".gz"):
                    out_name = path.stem
                    out_path = tmp_dir / out_name
                    with gzip.open(path, "rb") as src:
                        with open(out_path, "wb") as dst:
                            shutil.copyfileobj(src, dst)
                    members = [out_name]

                else:
                    return {
                        "success": False,
                        "text": "",
                        "metadata": {
                            "handler": "ArchiveHandler",
                            "error": "Unsupported archive format"
                        }
                    }

                for f in tmp_dir.rglob("*"):
                    if f.is_file():
                        rel = str(f.relative_to(tmp_dir))
                        extracted_preview.append(rel)

            text = "\n".join(extracted_preview)

            return {
                "success": True,
                "text": text,
                "metadata": {
                    "handler": "ArchiveHandler",
                    "members_count": len(members),
                    "members": members[:100],
                    "extracted_preview": extracted_preview[:100],
                    "note": "Archive was inspected and safely extracted to temporary folder only"
                }
            }

        except Exception as e:
            return {
                "success": False,
                "text": "",
                "metadata": {
                    "handler": "ArchiveHandler",
                    "error": str(e)
                }
            }

    def _safe_extract_zip(self, zf, target: Path):
        for member in zf.infolist():
            dest = (target / member.filename).resolve()
            if not str(dest).startswith(str(target.resolve())):
                raise RuntimeError(f"Unsafe zip path detected: {member.filename}")
            if not member.is_dir():
                dest.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member, "r") as src:
                    with open(dest, "wb") as dst:
                        shutil.copyfileobj(src, dst)

    def _safe_extract_tar(self, tf, target: Path):
        for member in tf.getmembers():
            dest = (target / member.name).resolve()
            if not str(dest).startswith(str(target.resolve())):
                raise RuntimeError(f"Unsafe tar path detected: {member.name}")
            if member.isfile():
                dest.parent.mkdir(parents=True, exist_ok=True)
                src = tf.extractfile(member)
                if src is not None:
                    with open(dest, "wb") as dst:
                        shutil.copyfileobj(src, dst)