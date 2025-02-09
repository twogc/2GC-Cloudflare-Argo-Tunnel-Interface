"""
    Фаил с дополнительными функциями.

Functions:
--------
    open_website(site_url): Открывает веб-сайт в браузере по умолчанию.

See Also
--------
    webbrowser: Библиотека для открытия сайта в основном браузере.
"""

import webbrowser
import os
import urllib.request

CLOUDFLARED_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
CLOUDFLARED_PATH = "win/cloudflared.exe"

def download_cloudflared():
    """Скачивает cloudflared.exe, если его нет."""
    if not os.path.exists(CLOUDFLARED_PATH):
        print("🔽 Скачиваем cloudflared.exe...")
        urllib.request.urlretrieve(CLOUDFLARED_URL, CLOUDFLARED_PATH)
        print("✅ cloudflared.exe загружен!")

download_cloudflared()


def open_website(site_url:str) -> None:
    """
        Открывает веб-сайт в браузере по умолчанию.

    :param: site_url: (str) ссылка, которую нужно открыть.

    :return: None
    """
    webbrowser.open(site_url)
