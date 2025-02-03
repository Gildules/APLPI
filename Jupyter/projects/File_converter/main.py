import sys
import os

# Получаем абсолютный путь к папке src
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))

# Добавляем путь к src в sys.path, если его там ещё нет
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Импорт из пакета src
from gui.app import run_processing

if __name__ == "__main__":
    run_processing()