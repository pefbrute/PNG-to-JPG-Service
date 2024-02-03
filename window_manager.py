import subprocess
import time
from Xlib import X, display

def open_url(url="https://images.google.com", browser="vivaldi"):
    try:
        # Открываем URL в указанном браузере
        subprocess.Popen([browser, "--new-window", url])
        # Даём время на открытие окна браузера
        time.sleep(1)  # Подождите некоторое время, чтобы окно успело открыться
    except subprocess.CalledProcessError:
        print(f"Failed to open the URL in {browser}.")
    except Exception as e:
        print(f"Unexpected error when opening URL in {browser}: {e}")

def get_active_window():
    d = display.Display()
    root = d.screen().root
    window_id = root.get_full_property(d.intern_atom('_NET_ACTIVE_WINDOW'), X.AnyPropertyType).value[0]
    window = d.create_resource_object('window', window_id)
    
    try:
        window_name = window.get_wm_name()  # Получаем имя окна
        window_class = window.get_wm_class()  # Получаем класс окна
        
        print(f"Active window ID: {window_id}")
        print(f"Active window name: {window_name}")
        if window_class:  # Класс окна может быть None, поэтому проверяем перед печатью
            print(f"Active window class: {window_class[0]}, {window_class[1]}")
    except Exception as e:
        print(f"Error getting window name or class: {e}")
    
    return window

def resize_and_move_window(window, width, height, x, y):
    try:
        print(f"Resizing and moving window to width: {width}, height: {height}, x: {x}, y: {y}")
        subprocess.call(["wmctrl", "-r", ":ACTIVE:", "-b", "remove,maximized_vert,maximized_horz"])
        window.configure(width=width, height=height, x=x, y=y)
        window.display.flush()
        print("Window configuration applied.")
    except Exception as e:
        print(f"Failed to resize or move window. Error: {e}")
