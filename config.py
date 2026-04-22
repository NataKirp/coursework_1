from pathlib import Path

# 1. Задаем корень проекта (папка, где лежит этот файл)
BASE_DIR = Path(__file__).resolve().parent

# 2. Определяем папки (относительно корня)
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'

# 3. Определяем конкретные файлы
EXCEL_DATA = DATA_DIR / 'operations.xlsx'
USER_SETT_PATH = BASE_DIR / 'user_settings.json'

# 4. Полезный лайфхак: создаем папки автоматически, если их нет
# DATA_DIR.mkdir(exist_ok=True)
# LOGS_DIR.mkdir(exist_ok=True)