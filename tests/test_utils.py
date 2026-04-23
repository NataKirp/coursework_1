from pathlib import Path

import pandas as pd
import pytest
from freezegun import freeze_time

from src.utils import get_greeting, read_excel_file


@freeze_time("2020-05-20 06:00:00")
def test_get_greeting_morning():
    """Тестирование корректного определения интервала времени при выводе приветствия"""
    assert get_greeting() == "Доброе утро"


@freeze_time("2020-05-20 20:00:00")
def test_get_greeting_evening():
    """Тестирование корректного определения интервала времени при выводе приветствия"""
    assert get_greeting() == "Добрый вечер"


@freeze_time("2020-05-20 01:00:00")
def test_get_greeting_night():
    """Тестирование корректного определения интервала времени при выводе приветствия"""
    assert get_greeting() == "Доброй ночи"


def test_read_excel_success(tmp_path):
    """Тестирование корректного чтения и фильтрации по статусу ОК."""
    file_path = tmp_path / "temp.xlsx"
    data = pd.DataFrame({"Статус": ["OK", "ERROR", "OK"], "Сумма": [100, 200, 300]})
    data.to_excel(file_path, index=False)

    result = read_excel_file(file_path)

    assert len(result) == 2
    assert all(result["Статус"] == "OK")


def test_read_excel_file_not_found():
    """Тестирование на отсутствие файла."""
    with pytest.raises(FileNotFoundError):
        read_excel_file(Path("non_existent_file.xlsx"))


def test_read_excel_wrong_extension(tmp_path):
    """Тест на неверное расширение."""
    bad_file = tmp_path / "data.txt"
    bad_file.write_text("some data")

    with pytest.raises(ValueError, match="Файл должен иметь формат .xlsx"):
        read_excel_file(bad_file)
