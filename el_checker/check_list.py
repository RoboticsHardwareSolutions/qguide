import os
from pathlib import Path


def _die(message: str) -> None:
    # Единая точка выхода с сообщением об ошибке
    print(message)
    raise SystemExit(1)


def _list_names(dir_path: Path) -> set[str]:
    # Возвращает множество имён (файлы/папки) внутри директории
    try:
        return {p.name for p in dir_path.iterdir()}
    except FileNotFoundError:
        _die(f"Папка не найдена: {dir_path}")


def _assert_required(names: set[str], required: set[str], message: str) -> None:
    # Проверяем, что все обязательные элементы присутствуют
    if not required.issubset(names):
        _die(message)


def _expect_exactly_one(names: set[str], predicate, message: str) -> str:
    # Ищем ровно один файл по условию (например, один .qet / один .pdf / один .csv)
    matches = [n for n in names if predicate(n)]
    if len(matches) != 1:
        _die(message)
    return matches[0]


def _expect_at_least(names: set[str], predicate, count: int, message: str) -> None:
    # Проверяем, что файлов по условию не меньше заданного количества (например, минимум 3 превью .png)
    matches = [n for n in names if predicate(n)]
    if len(matches) < count:
        _die(message)


def _check_no_trash(where: str, names: set[str], allowed: set[str]) -> None:
    # “Мусор” — всё, что не входит в белый список allowed
    trash = sorted(names - allowed)
    if trash:
        print(f"В {where} репозитория содержится 'мусор' :")
        print(trash)
        raise SystemExit(1)


def check_list(vault: str) -> None:
    # vault — путь к корню репозитория (папка проекта)
    vault_path = Path(vault)
    doc_path = vault_path / "doc"
    previews_path = doc_path / "schematic_previews"

    # Проверка базовой структуры папок
    root_names = _list_names(vault_path)
    _assert_required(root_names, {"doc"}, "Папка /doc отсутствует в корне репозитория")

    doc_names = _list_names(doc_path)
    _assert_required(
        doc_names,
        {"schematic_previews"},
        "Папка /doc/schematic_previews отсутствует в корне репозитория",
    )

    # В корне должен быть ровно один файл проекта .qet
    project_file = _expect_exactly_one(
        root_names,
        lambda n: n.lower().endswith(".qet"),
        "В корневой директории отсутствует файл проекта или содержится несколько проектов",
    )

    # В /doc должны быть ровно одна спецификация .csv и ровно один pdf схемы
    spec_file = _expect_exactly_one(
        doc_names,
        lambda n: n.lower().endswith(".csv"),
        "В директории /doc отсутствует файл спецификации или содержится несколько файлов",
    )

    pdf_file = _expect_exactly_one(
        doc_names,
        lambda n: n.lower().endswith(".pdf"),
        "В директории /doc отсутствует файл схемы или содержится несколько файлов",
    )

    # В /doc/schematic_previews должно быть минимум 3 png
    previews_names = _list_names(previews_path)
    _expect_at_least(
        previews_names,
        lambda n: n.lower().endswith(".png"),
        3,
        "В директории /doc/schematic_previews отсутствуют превью листов схемы в формате .png",
    )

    # Белый список допустимых файлов/папок в корне
    allowed_root = {
        "doc",
        project_file,
        "README.md",
        "Readme.md",
        ".git",
        ".gitlab-ci.yml",
        ".gitignore",
        ".DS_Store",
        "simulation",
        ".gitmodules",
        "software",
        "firmware",
    }
    _check_no_trash("корне", root_names, allowed_root)

    # Белый список допустимых файлов/папок в /doc
    allowed_doc = {spec_file, pdf_file, "schematic_previews", ".DS_Store"}
    _check_no_trash("папке /doc", doc_names, allowed_doc)


def get_vault_test():
    return "/Users/doc/projects/dm/server-cabinet/"


if __name__ == "__main__":
    # Локальный ручной запуск проверки
    check_list(get_vault_test())
