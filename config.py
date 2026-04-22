from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'

EXCEL_DATA = DATA_DIR / 'operations.xlsx'
USER_SETT_PATH = BASE_DIR / 'user_settings.json'
