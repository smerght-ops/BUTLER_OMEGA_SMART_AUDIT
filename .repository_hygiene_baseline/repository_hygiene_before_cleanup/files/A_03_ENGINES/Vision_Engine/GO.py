from pathlib import Path

def process_image(file_path):
    # Приводим к абсолютному пути, чтобы избежать ошибки relative_to
    file_path = Path(file_path).resolve()
    project_root = Path(__file__).resolve().parent.parent.parent
    
    # ПРЕДОХРАНИТЕЛЬ: Если это не картинка или путь не внутри проекта - пропускаем Vision
    if not file_path.exists() or file_path.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp'}:
        return "TEXT_MODE_ONLY"
    
    # Теперь, когда путь абсолютный, relative_to сработает корректно
    try:
        rel_path = file_path.relative_to(project_root)
    except ValueError:
        return "TEXT_MODE_ONLY" # Файл вне проекта - Vision его не трогает
    
    return "ANALYZED"
