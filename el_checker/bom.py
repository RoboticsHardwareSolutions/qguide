import csv
import os

# Какие столбцы обязательны (и должны быть непустыми в каждой строке данных)
REQUIRED_NON_EMPTY = ("Textual description", "Article number", "Manufacturer", "Designation quantity")

# Какие заголовки должны присутствовать в файле (порядок не важен)
REQUIRED_HEADERS = (
    "Textual description",
    "Article number",
    "Manufacturer",
    "Quantity",
    "Unity",
    "Designation quantity",
)


def _die(message: str) -> None:
    """Единая точка выхода с сообщением об ошибке."""
    print(message)
    raise SystemExit(1)


def _find_bom(bom_directory: str) -> str | None:
    """Ищем BOM CSV в папке: имя начинается с 'parts list' и содержит '.csv'."""
    for name in os.listdir(bom_directory):
        if name.startswith("parts list") and ".csv" in name:
            return name
    return None


def _read_rows(csv_path: str) -> list[list[str]]:
    """Читаем CSV в список строк (каждая строка — список ячеек)."""
    with open(csv_path, newline="", encoding="UTF-8") as f:
        return list(csv.reader(f, delimiter=";", quotechar='"'))


def _header_index(rows: list[list[str]]) -> dict[str, int]:
    """
    Строим индекс заголовков: {название_столбца: индекс}.
    Проверяем наличие обязательных заголовков.
    """
    if not rows:
        _die(" BOM CSV пустой файл")

    header = rows[0]
    index = {name: i for i, name in enumerate(header) if name}

    missing = [h for h in REQUIRED_HEADERS if h not in index]
    if missing:
        print(" В таблице с bom содержатся неверные названия заголовков столбцов или не хватает столбцов.")
        print(" Ожидаются заголовки:", ", ".join(REQUIRED_HEADERS))
        print(" Не найдены:", ", ".join(missing))
        _die(" Исправьте заголовки в BOM")

    return index


def _get_cell(rows: list[list[str]], row_i: int, col_i: int, col_name: str) -> str:
    """Безопасное чтение ячейки: если строка короткая — понятная ошибка вместо IndexError."""
    if col_i >= len(rows[row_i]):
        print(" В таблице bom обнаружена строка с недостаточным количеством столбцов")
        print(f" Строка CSV: {row_i + 1} (нумерация как в файле, включая заголовок)")
        print(f" Требуется столбец '{col_name}', но в строке только {len(rows[row_i])} столбцов.")
        _die(" Проверьте разделители ';' и кавычки в CSV (все строки должны иметь одинаковое число столбцов).")
    return rows[row_i][col_i]


def _is_blank(value: str) -> bool:
    """Пусто = пустая строка или строка из пробелов/табов."""
    return value.strip() == ""


def _check_required_non_empty(rows: list[list[str]], idx: dict[str, int]) -> None:
    """Проверяем, что обязательные поля заполнены во всех строках данных."""
    if len(rows) < 2:
        _die(" В таблице bom не хватает данных")

    for col_name in REQUIRED_NON_EMPTY:
        col_i = idx[col_name]
        for r in range(1, len(rows)):
            value = _get_cell(rows, r, col_i, col_name)
            if _is_blank(value):
                _die(f" В таблице bom есть незаполненные поля {col_name}")


def _check_article_duplicates(rows: list[list[str]], idx: dict[str, int]) -> None:
    """Проверяем дубликаты артикулов (пробелы внутри артикула игнорируются)."""
    col_i = idx["Article number"]
    seen: set[str] = set()

    for r in range(1, len(rows)):
        raw = _get_cell(rows, r, col_i, "Article number")
        normalized = raw.replace(" ", "")
        if normalized in seen:
            print(" В списке артикулов есть дубликаты !!!")
            print(" Это может быть вызвано лишними пробелами до/после артикула или одинаковыми артикулами.")
            _die(" Требуется исправить в проекте !")
        seen.add(normalized)


def bom_check(bom_directory: str) -> None:
    """Главная проверка BOM."""
    bom_name = _find_bom(bom_directory)
    if bom_name is None:
        print(" Не найден файл BOM: ожидается CSV, имя которого начинается с 'parts list' в папке:")
        _die(f" {bom_directory}")

    bom_path = os.path.join(bom_directory, bom_name)
    rows = _read_rows(bom_path)

    idx = _header_index(rows)
    _check_required_non_empty(rows, idx)
    _check_article_duplicates(rows, idx)
