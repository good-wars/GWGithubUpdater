# GWGithubUpdater

Приложение для обновления сборки GW

---

# Хочу использовать для своих проектов!

Для этого:

1. скачайте исходники
2. Откройте `app.py`
3. Там найдите участок кода

   ```python
   GITHUB_URL = 'https://github.com/good-wars/WorldChanges/raw/refs/heads/main/'
   APPSETTINGS = """{"filesDir": ""}"""
   VERSIONS = """{"mods": "0.0.0","config": "0.0.0","scripts": "0.0.0","hollowengine": "0.0.0"}"""
   DIRS = ["mods", "config", "scripts", "hollowengine"]
   ```
   Там измените
   `GITHUB_URL = '<Своя ссылка>'`

   Ссылка на репозиторий Github или любую другую платформу с подержкой открытия файлов в формате raw!

   ```python
   VERSIONS = """{"<Название Зип архива БЕЗ .zip>": "0.0.0","<Название Зип архива БЕЗ .zip>": "0.0.0","<Название Зип архива БЕЗ .zip>": "0.0.0","<Название Зип архива БЕЗ .zip>": "0.0.0", "И так далее": "ВЕРСИЯ"}"""
   ```
   Название Зип архива БЕЗ .zip который на главной странице репозитоия
   `DIRS = ["mods", "config", "scripts", "hollowengine"]` Здесь в кавычках через запятую всё названия zip архивов БЕЗ .zip
4. В репозитории который вы указали в `GITHUB_URL`. Нужно закинуть ZIP архивы всех папок указанных выше
   **ВНИМАНИЕ**
   ZIP архив распаковывается без создания новых папок т.е. он распаковываеся как обычный ZIP архив
   Например:
   config.zip должен иметь внутри папку config!
   ![1728747671563](images/README/1728747671563.png)
   Что-бы получилось так после установки:
   ![1728747774736](images/README/1728747774736.png)
