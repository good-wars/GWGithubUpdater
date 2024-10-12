import time
from hurry.filesize import size
import customtkinter as ctk
from tkinter import filedialog
from tqdm import tqdm
import zipfile
import os
import requests
import json
import threading

GITHUB_URL = 'https://github.com/good-wars/WorldChanges/raw/refs/heads/main/'
APPSETTINGS = """{"filesDir": ""}"""
VERSIONS = """{"mods": "0.0.0","config": "0.0.0","scripts": "0.0.0","hollowengine": "0.0.0"}"""
DIRS = ["mods", "config", "scripts", "hollowengine"]
NAME = "GW Updater"
GEOMETRY = "400x300"
ICON = "GW.ico" 

class UpdaterApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title(NAME)
        self.geometry(GEOMETRY)
        self.after(10, lambda: self.iconbitmap(ICON))
        
        self.dir_path = ""
        self.create_app_settings()
        self.load_dir_path()
        
        self.create_widgets()
    
    def create_widgets(self):
        self.folder_label = ctk.CTkLabel(self, text="Выбранная папка:")
        self.folder_label.pack(pady=10)
        
        self.folder_path = ctk.CTkLabel(self, text=self.dir_path or "Не выбрана")
        self.folder_path.pack()
        
        self.select_folder_btn = ctk.CTkButton(self, text="Выбрать папку", command=self.select_folder)
        self.select_folder_btn.pack(pady=10)
        
        self.update_btn = ctk.CTkButton(self, text="Обновить", command=self.start_update)
        self.update_btn.pack(pady=10)
        
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)
    
    def create_app_settings(self):
        if not os.path.exists('AppSettings.json'):
            with open('AppSettings.json', 'w') as f:
                f.write(APPSETTINGS)
    
    def load_dir_path(self):
        with open('AppSettings.json') as f:
            config = json.load(f)
        self.dir_path = config['filesDir']
    
    def select_folder(self):
        self.dir_path = filedialog.askdirectory()
        if self.dir_path:
            self.folder_path.configure(text=self.dir_path)
            with open('AppSettings.json', 'w') as f:
                json.dump({"filesDir": self.dir_path}, f)
    
    def start_update(self):
        if not self.dir_path:
            self.status_label.configure(text="Выберите папку!")
            return
        threading.Thread(target=self.update_process).start()
    
    def update_process(self):
        self.create_versions_file()
        git = requests.get(f'{GITHUB_URL}/Versions.json').json()
        versions = self.get_versions()
        
        total_updates = sum(1 for dir_name in DIRS if versions[dir_name] != git[dir_name])
        completed_updates = 0
        
        for dir_name in DIRS:
            if versions[dir_name] != git[dir_name]:
                self.status_label.configure(text=f"Обновление {dir_name}...")
                new_version = self.download_and_extract(dir_name, git[dir_name])
                if new_version:
                    versions[dir_name] = new_version
                    completed_updates += 1
        
        self.update_versions(versions)
        self.status_label.configure(text="Обновление завершено!")
    
    def create_versions_file(self):
        if not os.path.exists(f'{self.dir_path}/Versions.json'):
            with open(f'{self.dir_path}/Versions.json', 'w') as f:
                f.write(VERSIONS)
    
    def get_versions(self):
        with open(f'{self.dir_path}/Versions.json') as f:
            return json.loads(f.read())
    
    def download_and_extract(self, dir_name, new_version):
        zip_url = f'{GITHUB_URL}{dir_name}.zip'
        response = requests.get(zip_url, stream=True)
        
        if response.status_code == 200:
            zip_path = f'{self.dir_path}/{dir_name}.zip'
            total_size = int(response.headers.get('content-length', 0))
            block_size = 32768
            written = 0
            start_time = time.time()
            
            with open(zip_path, 'wb') as file:
                for data in response.iter_content(block_size):
                    written += len(data)
                    file.write(data)
                    done = int(10 * written / total_size)
                    percent = (written / total_size) * 100
                    elapsed_time = time.time() - start_time
                    speed = written / (elapsed_time if elapsed_time > 0 else 1)
                    
                    progress_text = f"\rУстановка: {dir_name}:\n[{('⬛' * done)}{'⬜' * (10-done)}] {percent:.2f}% "
                    progress_text += f"| {size(written)}/{size(total_size)} | {size(speed)}/s"
                    
                    self.status_label.configure(text=progress_text)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.dir_path)
            
            os.remove(zip_path)
            return new_version
        else:
            self.status_label.configure(text=f"Ошибка загрузки {dir_name}.zip")
            return None
    
    def update_versions(self, versions):
        with open(f'{self.dir_path}/Versions.json', 'w') as f:
            json.dump(versions, f)

if __name__ == "__main__":
    try:
        app = UpdaterApp()
        app.mainloop()
    except Exception as e:
        import traceback
        with open("error_log.txt", "w") as f:
            f.write(str(e) + "\n" + traceback.format_exc())
