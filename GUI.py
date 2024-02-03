import os
import json
import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Label, filedialog
import pyperclip
from googletrans import Translator
import subprocess
import pyautogui
import time

import sys
sys.path.append('/home/pefbrute/.config/autokey/data/My Phrases/Скрипты и прочее1/Библиотеки')
from window_manager import open_url, get_active_window, resize_and_move_window

# Функция для перевода текста на английский
def translate_to_english(text):
    translator = Translator()
    return translator.translate(text, dest='en').text

# Функция для обработки закрытия окна
def on_close(root):
    root.destroy()

# Функция для отображения таймера
def show_timer(root, duration=7):
    timer_window = Toplevel(root)
    timer_window.title("Таймер")
    timer_label = Label(timer_window, text=f"До вставки текста осталось {duration} секунд")
    timer_label.pack()

    def update_timer():
        nonlocal duration
        duration -= 1
        if duration > 3:
            timer_label.config(text=f"До вставки текста осталось {duration} секунд")
            timer_window.after(1000, update_timer)
        elif duration == 3:
            timer_label.config(text="Вставка текста...")
            timer_window.after(1000, timer_window.destroy)

    timer_window.after(1000, update_timer)

# Функция для создания и обработки GUI
def ask_character_or_object():
    root = tk.Tk()
    root.withdraw()  # скрыть основное окно
    
    # Добавляем обработчик закрытия окна
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))

    # Функция для отображения диалоговых окон
    def showDialogs():
        character_or_object = translate_to_english(simpledialog.askstring("Ввод", "Какого персонажа или объект вы хотите сгенерировать?", parent=root))
        mood = translate_to_english(simpledialog.askstring("Ввод", "Какое настроение должно быть?", parent=root))
        suggestion_for_title = translate_to_english(simpledialog.askstring("Ввод", "Какое слово должно быть в названии?", parent=root))

        # Проверка, введено ли что-либо
        if character_or_object and mood:
            prompt = f"""
You are a creative GPT specialized in visualizing {mood.upper()} {character_or_object.upper()}.
Create image in vector style, just like on images I provided you with

MOOD SHOULD BE: {mood.upper()}

YOU SHOULD ALSO GENERATE CONTENT FOR JSON FILE
USE ONLY ENGLISH!!!

[
  
    'Format': 'Redbubble',
    'Title': [Engaging Informal Title in ENGLISH] (Up to 4 words. Should be something like that '{character_or_object}'. SHOULD INCLUDE THIS PHRASE '{suggestion_for_title}'),
    'Tags': [Engaging Tags in ENGLISH] (15 tags. EACH SHOULD BE UNIQUE. Example of 1 of them: '{character_or_object}'. Each separated by commas. Example: 'funny {character_or_object}', '{character_or_object} emotions),
    'Description': [Engaging Informal Description in ENGLISH] (The story behind the work in 2 sentences about how I wanted to make this work),
    'Media': (Select which 2 categories this image suits better: 1.Photography, 2. Design & Illustration, 3. Painting & Mixed Media, 4. Drawing, 5. Digital Art)
  ,  
    'Format': "TeePublic and Others",
    "Title": [Engaging Informal Title in ENGLISH] (Up to 4 words. Example: '{character_or_object}' or '{suggestion_for_title}'),
    "Main Tag": [Main Tag in ENGLISH] (1 tag. Example: '{character_or_object}')
    "Description": [Engaging Informal Description in ENGLISH] (The story behind the work in 2 sentences about how I wanted to make this work),
    "Supporting Tags": [Engaging Supporting Tags in ENGLISH] (14 tags. EACH SHOULD BE UNIQUE. Example of 1 of them: '{character_or_object}'. Each separated by commas.)
]
            """

            # Копирование текста в буфер обмена
            pyperclip.copy(prompt)
            
            # Открываем URL в браузере
            open_url("https://www.redbubble.com/portfolio/images/new?ref=account-nav-dropdown")
            # Получаем активное окно
            active_window = get_active_window()
            # Меняем размер и перемещаем окно
            resize_and_move_window(active_window, 800, 800, 0, 0)
            time.sleep(2)
            
            # Открываем URL в браузере
            open_url(f"https://www.google.com/search?q={mood} and {character_or_object} VECTOR ILLUSTRATION&sca_esv=602020555&hl=en&tbm=isch&sxsrf=ACQVn08-cUu0K8ZVTznDNyqfgxvDYw6AGw%3A1706377788065&source=hp&biw=1721&bih=990&ei=PEK1ZcTvAfP71e8PgcGFyA8&iflsig=ANes7DEAAAAAZbVQTF6actXntt8ZpJJW3MR0-i9FGaZm&ved=0ahUKEwjE_aHPkP6DAxXzffUHHYFgAfkQ4dUDCAc&uact=5&oq=Cute+and+Funny%2C+Nice+and+Rice+porridge+vector+illustration&gs_lp=EgNpbWciOkN1dGUgYW5kIEZ1bm55LCBOaWNlIGFuZCBSaWNlIHBvcnJpZGdlIHZlY3RvciBpbGx1c3RyYXRpb25IAFAAWABwAHgAkAEAmAEAoAEAqgEAuAEDyAEA-AEC-AEBigILZ3dzLXdpei1pbWc&sclient=img")
            # Получаем активное окно
            active_window = get_active_window()
            # Меняем размер и перемещаем окно
            resize_and_move_window(active_window, 800, 800, 0, 200)
            time.sleep(2)

            
            # Открываем URL в браузере
            open_url("https://chat.openai.com/g/g-pT1I8F71Z-obsuditel-2000")
            # Получаем активное окно
            active_window = get_active_window()
            # Меняем размер и перемещаем окно
            resize_and_move_window(active_window, 800, 800, 800, 200)
            time.sleep(2)
            
            delay = 12
                        
            # Отображение таймера
            show_timer(root, delay)

            # Запуск автоматического нажатия клавиш после задержки
            root.after(delay * 1000, lambda: pyautogui.hotkey('ctrl', 'v'))

        else:
            on_close(root)

    # Отложенный вызов функции showDialogs
    root.after(0, showDialogs)

    root.mainloop()

# Функция для копирования текста в буфер обмена
def copy_to_clipboard(text, root):
    root.clipboard_clear()
    root.clipboard_append(text)

# Функция для создания виджетов из данных JSON
def create_widgets_from_json(json_data, root):
    for item in json_data:
        first_property = True
        for key, value in item.items():
            if first_property:
                label = tk.Label(root, text=f"{key}: {value}")
                label.pack()
                first_property = False
            else:
                btn = tk.Button(root, text=key, command=lambda v=value: copy_to_clipboard(v, root))
                btn.pack()

# Объединенная функция сохранения описания и создания ГУИ-дерева
def save_and_load_description():
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    clipboard_content = pyperclip.paste()
    root = tk.Tk()
    root.withdraw()
    initial_directory = '/home/pefbrute/Pictures/Произведения на Продажу-2'
    file_path = filedialog.asksaveasfilename(initialdir=initial_directory, defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if not file_path:
        return

    with open(file_path, 'w') as file:
        file.write(clipboard_content)

    # Создаем новое окно для ГУИ-дерева
    gui_tree_root = tk.Tk()
    gui_tree_root.title("ГУИ Дерево из Описания")

    time.sleep(5)

    with open(file_path, 'r') as file:
        json_data = json.load(file)
        create_widgets_from_json(json_data, gui_tree_root)

    gui_tree_root.mainloop()
    
def load_description():
    root = tk.Tk()
    root.withdraw()
    initial_directory = '/home/pefbrute/Pictures/Произведения на Продажу-2'
    file_path = filedialog.asksaveasfilename(initialdir=initial_directory, defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if not file_path:
        return

    # Создаем новое окно для ГУИ-дерева
    gui_tree_root = tk.Tk()
    gui_tree_root.title("ГУИ Дерево из Описания")

    time.sleep(5)

    with open(file_path, 'r') as file:
        json_data = json.load(file)
        create_widgets_from_json(json_data, gui_tree_root)

    gui_tree_root.mainloop()

# Создание основного окна
root = tk.Tk()
root.title("Генератор изображений и описаний")

# Создание кнопок
btn_generate_image = tk.Button(root, text="Сгенерировать изображение", command=ask_character_or_object)
btn_generate_image.pack()

btn_save_and_load_description = tk.Button(root, text="Сохранить и загрузить описание", command=save_and_load_description)
btn_save_and_load_description.pack()

btn_load_description = tk.Button(root, text="Загрузить описание", command=load_description)
btn_load_description.pack()

# Запуск цикла событий
root.mainloop()
