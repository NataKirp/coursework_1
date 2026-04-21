import logging

from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
logs_dir = root_dir / 'logs'
logs_dir.mkdir(parents=True, exist_ok=True)
dir_path = logs_dir


def setup_logging(module_name: str):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(f'{dir_path}/{module_name}.log', mode='w', encoding='utf-8')
    file_formatter = logging.Formatter('%(asctime)s : %(filename)s : %(levelname)s : %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    return logger
