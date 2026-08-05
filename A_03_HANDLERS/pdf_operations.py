from __future__ import annotations

import os
import re
import tempfile
import time
from pathlib import Path


class PDFOperationError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _absolute(path) -> Path:
    value = Path(str(path))
    if not value.is_absolute():
        # Convert relative path to absolute based on current working directory
        value = Path.cwd() / value
    return value


def _reader(path):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise PDFOperationError("PDF_DEPENDENCY_MISSING", "Библиотека pypdf недоступна.") from exc
    path = _absolute(path)
    if not path.exists():
        raise PDFOperationError("PDF_SOURCE_NOT_FOUND", f"PDF не найден: {path}")
    if not path.is_file():
        raise PDFOperationError("PDF_SOURCE_NOT_FILE", f"Путь не является файлом: {path}")
    if path.suffix.lower() != ".pdf":
        raise PDFOperationError("PDF_INVALID_DOCUMENT", f"Ожидался файл .pdf: {path}")
    try:
        reader = PdfReader(str(path))
        if reader.is_encrypted:
            try:
                if not reader.decrypt(""):
                    raise PDFOperationError("PDF_PASSWORD_REQUIRED", "PDF защищён паролем.")
            except PDFOperationError:
                raise
            except Exception as exc:
                raise PDFOperationError("PDF_PASSWORD_REQUIRED", "PDF защищён паролем.") from exc
        if not reader.pages:
            raise PDFOperationError("PDF_INVALID_DOCUMENT", "PDF не содержит страниц.")
        return path, reader
    except PDFOperationError:
        raise
    except Exception as exc:
        raise PDFOperationError("PDF_INVALID_DOCUMENT", f"PDF повреждён или не открывается: {path}") from exc


def _target(path, suffix=".pdf") -> Path:
    path = _absolute(path)
    if suffix and path.suffix.lower() != suffix:
        raise PDFOperationError("PDF_INVALID_DOCUMENT", f"Целевой файл должен иметь расширение {suffix}: {path}")
    if path.exists():
        raise PDFOperationError("PDF_TARGET_EXISTS", f"Целевой путь уже существует: {path}")
    return path


def parse_pages(spec: str, count: int, *, allow_duplicates=False):
    if not spec or not re.fullmatch(r"\s*\d+(?:\s*-\s*\d+)?(?:\s*,\s*\d+(?:\s*-\s*\d+)?)*\s*", spec):
        raise PDFOperationError("PDF_INVALID_PAGE_SPEC", f"Некорректный список страниц: {spec}")
    result = []
    for part in spec.split(","):
        bounds = [int(x.strip()) for x in part.split("-")]
        if len(bounds) == 2 and bounds[0] > bounds[1]:
            raise PDFOperationError("PDF_INVALID_PAGE_SPEC", f"Некорректный диапазон: {part}")
        values = range(bounds[0], bounds[-1] + 1)
        for number in values:
            if number < 1 or number > count:
                raise PDFOperationError("PDF_PAGE_OUT_OF_RANGE", f"Страница {number} вне диапазона 1-{count}.")
            if not allow_duplicates and number in result:
                raise PDFOperationError("PDF_INVALID_PAGE_SPEC", f"Страница {number} указана повторно.")
            result.append(number)
    return result


def _atomic_writer(writer, target: Path):
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent))
    os.close(fd)
    tmp = Path(tmp_name)
    try:
        with tmp.open("wb") as stream:
            writer.write(stream)
        _, check = _reader_temp(tmp)
        if not check.pages:
            raise PDFOperationError("PDF_OPERATION_FAILED", "Созданный PDF не прошёл проверку.")
        os.replace(str(tmp), str(target))
    finally:
        if tmp.exists():
            tmp.unlink()


def _reader_temp(path):
    from pypdf import PdfReader
    try:
        reader = PdfReader(str(path))
        return path, reader
    except Exception as exc:
        raise PDFOperationError("PDF_OPERATION_FAILED", "Созданный PDF не открывается.") from exc


def _writer_for(reader, pages):
    from pypdf import PdfWriter
    writer = PdfWriter()
    for number in pages:
        writer.add_page(reader.pages[number - 1])
    return writer


def info(source):
    path, reader = _reader(source)
    metadata = reader.metadata or {}
    return {"operation": "info", "source_paths": [str(path)], "source_page_count": len(reader.pages),
            "output_page_count": len(reader.pages), "output_size_bytes": path.stat().st_size,
            "pdf_metadata": {str(k).lstrip("/"): str(v) for k, v in metadata.items()},
            "encrypted": bool(reader.is_encrypted)}


def merge(sources, target):
    if len(sources) < 2:
        raise PDFOperationError("PDF_MERGE_REQUIRES_MULTIPLE_SOURCES", "Нужно минимум два PDF.")
    target = _target(target)
    from pypdf import PdfWriter
    writer, paths, total = PdfWriter(), [], 0
    for source in sources:
        path, reader = _reader(source); paths.append(str(path)); total += len(reader.pages)
        for page in reader.pages: writer.add_page(page)
    _atomic_writer(writer, target)
    return {"operation": "merge", "source_paths": paths, "target_path": str(target), "source_page_count": total,
            "output_page_count": total, "output_size_bytes": target.stat().st_size}


def select(source, target, spec, operation="extract", rotation=None, allow_duplicates=False):
    path, reader = _reader(source); target = _target(target)
    pages = parse_pages(spec, len(reader.pages), allow_duplicates=allow_duplicates)
    if operation == "remove":
        removed = pages; pages = [n for n in range(1, len(reader.pages)+1) if n not in removed]
        if not pages: raise PDFOperationError("PDF_EMPTY_RESULT_FORBIDDEN", "Нельзя удалить все страницы PDF.")
    writer = _writer_for(reader, pages)
    if operation == "rotate":
        if rotation not in {90, 180, 270, -90, -180, -270}:
            raise PDFOperationError("PDF_INVALID_ROTATION", f"Недопустимый угол: {rotation}")
        writer = _writer_for(reader, range(1, len(reader.pages)+1))
        for number in pages: writer.pages[number-1].rotate(rotation)
    _atomic_writer(writer, target)
    data = {"operation": operation, "source_paths": [str(path)], "target_path": str(target),
            "source_page_count": len(reader.pages), "output_page_count": len(writer.pages),
            "selected_pages": pages, "output_size_bytes": target.stat().st_size}
    if operation == "remove": data.update(removed_pages=removed, selected_pages=[])
    if operation == "rotate": data["rotation"] = rotation
    return data


def reorder(source, target, spec):
    path, reader = _reader(source); target = _target(target)
    pages = parse_pages(spec, len(reader.pages), allow_duplicates=True)
    if not pages: raise PDFOperationError("PDF_EMPTY_RESULT_FORBIDDEN", "Пустой результат запрещён.")
    writer = _writer_for(reader, pages); _atomic_writer(writer, target)
    return {"operation": "reorder", "source_paths": [str(path)], "target_path": str(target),
            "source_page_count": len(reader.pages), "output_page_count": len(pages), "selected_pages": pages,
            "output_size_bytes": target.stat().st_size}


def split(source, folder, specs=None, selected=None):
    path, reader = _reader(source); folder = _absolute(folder)
    groups = [parse_pages(x.strip(), len(reader.pages)) for x in specs.split(",")] if specs else [[n] for n in (parse_pages(selected, len(reader.pages)) if selected else range(1, len(reader.pages)+1))]
    names = []
    for index, pages in enumerate(groups, 1):
        if specs: name = f"part_{index:03d}_{'page' if len(pages)==1 else 'pages'}_{pages[0]}" + (f"-{pages[-1]}" if len(pages)>1 else "") + ".pdf"
        else: name = f"page_{pages[0]:03d}.pdf"
        names.append(folder / name)
    if any(x.exists() for x in names): raise PDFOperationError("PDF_TARGET_EXISTS", "Один или несколько целевых файлов уже существуют.")
    folder.mkdir(parents=True, exist_ok=True)
    created=[]
    try:
        for pages, target in zip(groups, names): _atomic_writer(_writer_for(reader, pages), target); created.append(target)
    except Exception:
        for target in created:
            if target.exists(): target.unlink()
        raise
    return {"operation": "split", "source_paths": [str(path)], "target_path": str(folder),
            "source_page_count": len(reader.pages), "output_page_count": sum(map(len, groups)),
            "created_files": [str(x) for x in names]}


def images_to_pdf(sources, target):
    try:
        from PIL import Image
    except ImportError as exc: raise PDFOperationError("PDF_DEPENDENCY_MISSING", "Pillow недоступна.") from exc
    target = _target(target); paths=[]; images=[]
    try:
        for source in sources:
            path=_absolute(source)
            if not path.exists(): raise PDFOperationError("PDF_SOURCE_NOT_FOUND", f"Изображение не найдено: {path}")
            if not path.is_file(): raise PDFOperationError("PDF_SOURCE_NOT_FILE", f"Путь не является файлом: {path}")
            if path.suffix.lower() not in {".png", ".jpg", ".jpeg"}: raise PDFOperationError("PDF_INVALID_DOCUMENT", f"Неподдерживаемое изображение: {path}")
            image=Image.open(path); image.load(); images.append(image.convert("RGB")); paths.append(str(path))
        if not images: raise PDFOperationError("PDF_NO_INPUT_IMAGES", "Нет входных изображений.")
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent))
        os.close(fd); tmp = Path(tmp_name)
        images[0].save(tmp, "PDF", save_all=True, append_images=images[1:])
        _reader_temp(tmp); os.replace(str(tmp), str(target))
    except Exception:
        if target.exists(): target.unlink()
        if 'tmp' in locals() and tmp.exists(): tmp.unlink()
        raise
    finally:
        for image in images: image.close()
    return {"operation": "images_to_pdf", "source_paths": paths, "target_path": str(target),
            "output_page_count": len(paths), "output_size_bytes": target.stat().st_size}


def folder_to_pdf(folder, target):
    folder=_absolute(folder)
    if not folder.exists(): raise PDFOperationError("PDF_SOURCE_NOT_FOUND", f"Папка не найдена: {folder}")
    if not folder.is_dir(): raise PDFOperationError("PDF_SOURCE_NOT_FILE", f"Ожидалась папка: {folder}")
    def key(p): return [int(x) if x.isdigit() else x.casefold() for x in re.split(r"(\d+)", p.name)]
    paths=sorted((p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in {'.png','.jpg','.jpeg'}), key=key)
    if not paths: raise PDFOperationError("PDF_NO_INPUT_IMAGES", "В папке нет изображений.")
    return images_to_pdf(paths, target)


def text_to_pdf(text, target):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen.canvas import Canvas
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError as exc: raise PDFOperationError("PDF_DEPENDENCY_MISSING", "reportlab недоступна.") from exc
    target=_target(target); target.parent.mkdir(parents=True, exist_ok=True)
    fd,tmp_name=tempfile.mkstemp(prefix=f".{target.name}.", suffix='.tmp', dir=str(target.parent)); os.close(fd)
    tmp=Path(tmp_name)
    try:
        # Try to use a font that supports Cyrillic
        font_path = None
        import sys
        for search_path in [r'C:\Windows\Fonts\arialuni.ttf', r'C:\Windows\Fonts\times.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
            if Path(search_path).exists():
                font_path = search_path
                break

        canvas=Canvas(str(tmp), pagesize=A4)
        width,height=A4; y=height-50; pages=1

        # Use Helvetica with encoding that supports Cyrillic if available, otherwise use default
        try:
            if font_path and Path(font_path).exists():
                pdfmetrics.registerFont(TTFont('Cyrillic', font_path))
                current_font = 'Cyrillic'
            else:
                current_font = 'Helvetica'
        except Exception:
            current_font = 'Helvetica'

        for paragraph in (text.splitlines() or [""]):
            words=paragraph.split(); line=""
            lines=[]
            for word in words:
                candidate=(line+" "+word).strip()
                if canvas.stringWidth(candidate, current_font, 11)>width-100: lines.append(line); line=word
                else: line=candidate
            lines.append(line)
            for value in lines:
                if y<50: canvas.showPage(); pages+=1; y=height-50
                canvas.drawString(50,y,value); y-=15
            y-=5
        canvas.save(); _reader_temp(tmp); os.replace(str(tmp),str(target))
    finally:
        if tmp.exists(): tmp.unlink()
    return {"operation":"text_to_pdf", "source_paths":[], "target_path":str(target), "output_page_count":pages,
            "output_size_bytes":target.stat().st_size}


def convert_docx_to_pdf(source, target):
    """
    Конвертирует DOCX файл в PDF с использованием LibreOffice headless mode.

    Args:
        source: Путь к входному DOCX файлу
        target: Путь к выходному PDF файлу (должен иметь .pdf расширение)

    Returns:
        dict: Метаданные операции

    Raises:
        PDFOperationError: Если конвертация не удалась
    """
    import subprocess
    import sys
    from pathlib import Path

    source = _absolute(source)
    if not source.exists():
        raise PDFOperationError("PDF_SOURCE_NOT_FOUND", f"DOCX файл не найден: {source}")
    if source.suffix.lower() != ".docx":
        raise PDFOperationError("PDF_INVALID_DOCUMENT", f"Ожидался файл .docx: {source}")

    target = _target(target, suffix=".pdf")
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to", "pdf",
                "--outdir", str(target.parent),
                str(source)
            ],
            capture_output=True,
            timeout=120
        )

        if result.returncode != 0:
            error_msg = result.stderr.decode("utf-8", errors="ignore") or result.stdout.decode("utf-8", errors="ignore")
            raise PDFOperationError("PDF_CONVERSION_FAILED", f"LibreOffice вернул ошибку {result.returncode}: {error_msg}")

        expected_pdf = target.parent / (source.stem + ".pdf")
        if not expected_pdf.exists():
            raise PDFOperationError("PDF_CONVERSION_FAILED", "LibreOffice не создал ожидаемый PDF файл.")

        os.replace(str(expected_pdf), str(target))
        _reader(target)

        return {
            "operation": "convert_docx_to_pdf",
            "source_path": str(source),
            "target_path": str(target),
            "output_page_count": len(_reader(target)[1].pages),
            "output_size_bytes": target.stat().st_size
        }
    except subprocess.TimeoutExpired:
        raise PDFOperationError("PDF_CONVERSION_TIMEOUT", "Конвертация заняла слишком много времени.")
    except FileNotFoundError:
        raise PDFOperationError("LIBREOFFICE_NOT_FOUND", "LibreOffice не найден. Установите LibreOffice для конвертации DOCX→PDF.")
    except Exception as exc:
        raise PDFOperationError("PDF_CONVERSION_FAILED", f"Ошибка конвертации: {exc}") from exc


def unsupported_export(*_):
    try: import fitz  # noqa
    except ImportError: raise PDFOperationError("PDF_EXPORT_NOT_SUPPORTED", "Экспорт требует PyMuPDF.")


def unsupported_embedded(*_):
    try: import fitz  # noqa
    except ImportError: raise PDFOperationError("PDF_EMBEDDED_IMAGES_NOT_AVAILABLE", "Извлечение изображений требует PyMuPDF.")
