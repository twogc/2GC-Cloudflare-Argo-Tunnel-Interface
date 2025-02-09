import os
import sys
import subprocess
import psutil
from PyQt5.QtWidgets import QApplication

from controller import Controller
from views import MainView, Connector
from db.db_connector import SqliteDBConnect


def get_cloudflared_path():
    """Определяет путь к cloudflared.exe в зависимости от режима работы."""
    if getattr(sys, 'frozen', False):
        # PyInstaller упаковывает файлы в _MEIPASS
        base_path = sys._MEIPASS
    else:
        # В режиме разработки используется обычный путь
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, "cloudflared.exe")


class App(QApplication):
    """Класс для запуска приложения."""
    
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        version = "2.0.0"
        site_url = "https://2gc.io/"
        url_views = "2gc.io"
        self.model = SqliteDBConnect()
        self.main_view = MainView(version, url_views, site_url)
        self.connect_view = Connector(version, url_views, site_url)
        self.controller = Controller(self.model, self.main_view, self.connect_view)

        # Запуск cloudflared
        cloudflared_path = get_cloudflared_path()
        if os.path.exists(cloudflared_path):
            subprocess.Popen([cloudflared_path, "tunnel", "--url", "http://localhost:5000"])
        else:
            print(f"Ошибка: cloudflared.exe не найден по пути {cloudflared_path}")

        self.main_view.show()
        self.main_view.setWindowTitle("2GC Free")


def pre_init():
    """Проверяет, не запущено ли уже приложение."""
    try:
        processes = psutil.process_iter(['pid', 'name'])
        count = sum(1 for proc in processes if proc.info['name'] == "2gc.exe")
        return count <= 2
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


if __name__ == '__main__':
    if pre_init():
        app = App(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        sys.exit(app.exec_())