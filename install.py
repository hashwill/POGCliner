#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LauncherPOG - POGCliner Startup Installer
Добавляет приложение в автозагрузку Windows
"""

import winreg
import os
import sys
import tkinter as tk
from tkinter import messagebox

def add_to_startup():
    """Добавить POGCliner в автозагрузку"""
    
    # Получить путь текущего пользователя
    username = os.getenv('USERNAME')
    desktop_path = f"C:\\Users\\{username}\\Desktop"
    
    # Точный путь на рабочем столе
    exe_path = os.path.join(desktop_path, "POGCliner-main", "PitOfGoblinSetup", "POGCliner.exe")
    
    # Проверить существование файла
    if not os.path.exists(exe_path):
        return False, f"Файл не найден:\n{exe_path}"
    
    try:
        # Открыть реестр
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, 
            registry_path, 
            0, 
            winreg.KEY_WRITE
        )
        
        # Добавить значение с полным путём
        winreg.SetValueEx(
            registry_key, 
            "POGCliner", 
            0, 
            winreg.REG_SZ, 
            exe_path
        )
        
        winreg.CloseKey(registry_key)
        return True, "Успешно"
        
    except PermissionError:
        return False, "Недостаточно прав.\nЗапустите от администратора!"
    except Exception as e:
        return False, f"Ошибка: {e}"

def create_gui():
    """Создать GUI окошко"""
    
    # Создать главное окно
    root = tk.Tk()
    root.title("LauncherPOG")
    root.geometry("500x250")
    root.resizable(False, False)
    
    # Установить синий фон
    root.configure(bg="#1e3a5f")
    
    # Центрировать окно на экране
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')
    
    # Заголовок
    title_label = tk.Label(
        root,
        text="LauncherPOG",
        font=("Arial", 18, "bold"),
        fg="white",
        bg="#1e3a5f"
    )
    title_label.pack(pady=15)
    
    # Основное сообщение
    message_label = tk.Label(
        root,
        text="Файл установлен,\nзапустите его в папке PitOfGoblinSetup",
        font=("Arial", 12),
        fg="white",
        bg="#1e3a5f",
        justify="center"
    )
    message_label.pack(pady=20)
    
    # Кнопка закрытия
    def on_close():
        # Добавить в автозагрузку при закрытии
        success, msg = add_to_startup()
        if not success:
            messagebox.showerror("Ошибка", msg)
        root.quit()
    
    close_btn = tk.Button(
        root,
        text="Закрыть",
        command=on_close,
        bg="#0084d0",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=30,
        pady=10,
        border=0,
        cursor="hand2"
    )
    close_btn.pack(pady=30)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
