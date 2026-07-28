import os
from pathlib import Path


def get_schematic_previews(vault: str) -> list[str]:
    """Получить список изображений схем."""
    previews_dir = Path(vault) / "doc" / "schematic_previews"
    if not previews_dir.exists():
        return []

    pictures = [p for p in os.listdir(previews_dir) if not p.startswith('.')]
    return sorted(pictures)


def create_title(vault: str) -> str:
    """Создать заголовок из имени папки."""
    path = Path(vault).resolve()
    name = path.name.replace("_", " ").replace("-", " ").upper()
    return f"## {name}"


def sort_by_numeric_prefix(pictures: list[str]) -> tuple[list[str], list[str]]:
    """Разделить изображения на X_ и XX_ по префиксу."""
    pic_x = [p for p in pictures if p[0].isdigit() and not p[1].isdigit()]
    pic_xx = [p for p in pictures if p[0].isdigit() and p[1].isdigit()]
    return sorted(pic_x), sorted(pic_xx)


def write_readme(vault: str) -> None:
    """Сгенерировать README.md с превью схем."""
    vault_path = Path(vault)

    # Удаляем старый README
    for readme_name in ["Readme.md", "README.md"]:
        (vault_path / readme_name).unlink(missing_ok=True)

    # Генерируем новый
    readme_path = vault_path / "README.md"
    title = create_title(vault)
    pictures = get_schematic_previews(vault)
    pic_x, pic_xx = sort_by_numeric_prefix(pictures)

    lines = [title, ""]
    for p in pic_x + pic_xx:
        lines.append(f"![pic](doc/schematic_previews/{p})    ")

    readme_path.write_text("\n".join(lines) + "\n")


def get_vault_arg() -> str:
    """Получить путь к vault из аргументов командной строки."""
    if len(sys.argv) < 2:
        print("Ошибка: не указан путь к vault")
        sys.exit(1)

    path = sys.argv[1]
    return str(Path(path).resolve()) + "/"


if __name__ == '__main__':
    import sys

    print("Electrical Readme generator")
    vault = get_vault_arg()
    write_readme(vault)
    print("Файл README.md готов")
