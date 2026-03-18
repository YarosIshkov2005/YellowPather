# README.md

# RU 🇷🇺:
## YellowPather версия 1.0.4 "Yellow Brick Road"

Дорогие ностальгирующие по Windows 7! Сегодня я хочу представить вам свой первый по-настоящему сложный проект: файловый менеджер (проводник), который я написал всего за 2-3 месяца, используя простые библиотеки, такие как Tkinter, Pathlib, Platform и др., а также собственную систему защиты YPACMv1 (YellowPather Access Control Manager версия 1), ранее известную как MDEFS. Репозиторий проекта доступен по ссылке: https://github.com/YarosIshkov2005/YellowPather.git

📑 Это проект с открытым исходным кодом (Open Source), поэтому каждый может внести свои изменения, улучшения, исправления и т.д. Ярослав Ишков 2026 ❤️

🔮 Что нового в версии 1.0.4:
> настройки: добавлено включение/отключение вставки имени выделенного объекта (не работает при переходе из папки в папку. Будет исправлено в версии 1.0.5).

> рекурсивный поиск: исправлена проблема с кнопкой create (кнопка отключается во время рекурсивного поиска).

---

## Раздел 1: Описание 📄

### Что это за программа 🖥

В этом проекте я попытался создать простой файловый проводник для Windows 7, который включает в себя следующие функции:

**1. Рекурсивный поиск по расширению**

*   `r_*.расширение` - (glob) ищет файлы с указанным расширением в текущем каталоге.
*   `r_**.расширение` - (rglob) рекурсивно обходит дерево каталогов, возвращая файлы от текущего местоположения до конечных точек.

**Синтаксис команды:**

*   `c:\Пользователи\ИмяПользователя\папка\r_*.py` - для Windows.
*   `/home/users/username/folder/r_*.py` - для MacOS/Linux.
    *   `c:\Пользователи\ИмяПользователя\` - корневой каталог файловой системы устройства.
    *   `папка\` - текущий каталог.
    *   `r_*.py` - где `r_*` — это имя команды, `.py` — шаблон поиска.

> **Примечание:** Файлы доступны только для поверхностного просмотра. Открытие/изменение файлов по умолчанию заблокировано в YellowPather для защиты системных ресурсов от внешнего вмешательства. Эта защита применяется ко всем типам поиска (начиная с версии 1.0.3 защиту можно отключить в настройках, нажав кнопку Changed).

> Ищите изображение с результатом в папке: `YellowPather/Screenshots/`.

**2. Режим командной строки**

В дополнение к рекурсивному поиску, YellowPather имеет встроенный режим командной строки. Для его активации выполните следующие шаги:

**Активация:** Введите следующую команду в поле ввода:

*   `c:\Пользователи\ИмяПользователя\cmd-parser:on` - Windows.
*   `/home/users/username/cmd-parser:on` - MacOS/Linux.

> **Назначение:** `cmd-parser:on` активирует режим командной строки. После этого в поле ввода должно отображаться:
> `cmd:/`
> `cmd:/` — это префикс, сигнализирующий об успешной активации командной строки.

**Команды:** В настоящее время доступны только 3 команды (в будущем планируется больше). Давайте рассмотрим синтаксис каждой:

*   `copy "источник" to "назначение"`
    *   **Что делает:** Копирует объект "источник" в папку "назначение", где "источник" — это путь к копируемому объекту, а "назначение" — путь к целевой папке.
*   `move "источник" to "назначение"`
    *   **Что делает:** Перемещает объект "источник" в папку "назначение".
*   `rename "источник" to "назначение"`
    *   **Что делает:** Переименовывает текущее имя объекта "источник" в новое имя "назначение". Например:
        *   `rename "music" to "Music"` = `music` —> `Music`

**Деактивация:** Чтобы вернуться в обычный режим, введите обратную команду:
*   `cmd-parser:off`

> **Ограничения:**
>
> *   **Объекты:** Поскольку парсер команд не поддерживает списки путей, операции могут выполняться только с одним объектом в одном каталоге.
> *   **Защита:** В режиме командной строки действует та же защита, что и для рекурсивного поиска.
> *   **Регистр символов:** Ключевые слова: `copy`, `move`, `rename`, `to` должны быть указаны только в нижнем регистре.
> *   **Обходной путь:** Если в имени объекта есть пробелы, заключите имя в одинарные или двойные кавычки или попробуйте работать с другими объектами.

**3. Пользовательские рабочие пространства 📁**

YellowPather предоставляет 2 уровня доступа:

*   **Системный доступ:**
    *   📁 `c:\Пользователи\ИмяПользователя\` - Windows.
    *   📁 `/home/users/username/` - MacOS/Linux.
*   **Внутренний доступ (chroot):**
    *   📁 `YellowPather/YellowPather/users/0/`

**Переключение между зонами:**
Для переключения на внутренний доступ необходимо выполнить следующие шаги:

**Активация:** Откройте файл конфигурации:
`YellowPather/YellowPather/config/system_paths.json`

> **Назначение:** `system_paths.json` предоставляет пользователю доступ ко всем уровням доступа через специальные флаги, которые мы сейчас и рассмотрим:
>
> *   `auto_detect`: (Уровень 1) Автоматически определяет путь к корневому каталогу на основе системных данных. Отключено по умолчанию. При включении другие флаги игнорируются.
> *   `root_path`: (Уровень 1) Работает почти так же, как `auto_detect`. Его отличие в том, что он определяет путь к корневому каталогу на основе имени ядра ОС, в отличие от `auto_detect`, который использует более сложный алгоритм определения. Отключено по умолчанию.
> *   `user_path`: (Уровень 2) Перемещает пользователя во внутреннюю папку `users/0/`, которая представляет собой изолированную песочницу пользователя. Отключено по умолчанию.
>     *   **Альтернатива:** Отключите все флаги; Уровень 2 будет активирован автоматически.
> *   `device_path`: (Уровень 1) Работает аналогично `auto_detect` и `root_path`. Определяет путь к корневой папке на основе абсолютного пути с использованием `parents`. Включено по умолчанию.

> Также существует режим ручного ввода. Для его активации отключите `auto_detect`, включите `root_path`, `user_path`, `device_path`, нажмите ОК во всплывающем окне (это напоминание о необходимости отключить параметры). Введите путь к внутреннему или внешнему накопителю (SD-карта или USB).

> **Ограничения:** Поскольку `users/0/` — изолированная папка, пользователь не имеет доступа к папке `users/` и папкам более высокого уровня из-за защиты Jail (изоляции).

---

## Раздел 2: Технические характеристики ⚙️

**1. Поддерживаемые ОС:**

*   🖥 Windows
*   🖥 MacOS
*   🖥 Linux
*   📱 Android (требуется Pydroid 3)

**2. Неподдерживаемые ОС:**

*   📱 IOS (отсутствует нативная поддержка Python)

**3. Взаимодействие с устройством и ОС:**

*   **Уровень 1 (Прямой доступ):** Основной способ взаимодействия программы с системой устройства. На этом уровне YellowPather использует стандартные библиотеки Python без дополнительных проверок безопасности. Большинство модулей и утилит работают на этом уровне.
*   **Уровень 2 (YPACM):** Более безопасный метод, так как использует проверки безопасности, основанные на данных ОС. Используется для задач, требующих осторожности при выполнении, например, для процесса создания нового каталога/файла, сортировки объектов. В этом случае используется вызов `bootstrap()` из YPACM. YPACM также запускает фоновое окно демона для отображения ошибок или уведомлений, требующих запуска из отдельного родительского окна.

P.S.: Я не знаю, зачем вам может понадобиться эта информация, но давайте оставим это для эстетики 🤣

**4. Ошибки и решения:**

* В программе могут быть небольшие баги или ошибки, так что будьте готовы к непредсказуемому поведению в определённых сценариях. Я постараюсь исправить их в будущих версиях.

**5. Зависимости:**

*   🐍 Python 3.8.10 +
*   🖼 Pillow 12.1.0
*   🖥 charset-normalizer 3.4.4

P.S. Зависимости можно установить одной командой: `pip install -r requirement.txt`

---

## Раздел 3: Запуск ✈️

1.  Откройте редактор кода (IDE).
2.  Если вы используете VSCode, выполните следующие шаги:
    *   Перейдите на вкладку **Get Started** (обычно открывается при запуске, если проект еще не открыт).
    *   Выберите опцию **Open Folder** (также можно использовать **Open Editors**).
3.  В открывшемся окне нажмите на папку с названием `YellowPather`, затем выберите её (VSCode автоматически откроет папку).
4.  Выберите файл с именем `main.py`.
5.  Запустите файл в редакторе.

P.S.: При желании вы также можете добавить YellowPather на рабочий стол, упаковав программу в `.exe` файл для Windows или в `.app` для MacOS и Linux.

**Предупреждение:** Не используйте Pyinstaller для упаковки YellowPather! Проблема в том, что Pyinstaller упаковывает программу целиком в один файл, что помешает пользователю получить доступ к пользовательским настройкам (`system_paths.json, settings.json`), а также к изолированным песочницам (`users/0/`) и т.д.

**Решение:** Используйте упаковщик с возможностью управления ресурсами программы, например: `cx_Freeze`.

---

## Раздел 4: История 📕

...Однажды, в начале декабря прошлого года, я писал один из своих многочисленных проектов — музыкальный плеер. Вообще, это был не совсем мой проект; я нашел его на каком-то сайте. Изучив код, я решил переписать его в более функциональное состояние, потому что исходный код был, скажем так, на троечку. Недолго думая, я начал переписывать код, и когда дело дошло до добавления иконок для кнопок, а также фоновой GIF-анимации, начались небольшие проблемы. Чтобы добавить даже одну иконку, мне сначала нужно было открыть браузер, ввести запрос в поле поиска, затем бесконечно прокручивать изображения, и не было гарантии, что подходящее изображение будет в формате PNG и без фона; в основном это были JPEG. Но это было еще не всё. Если я находил JPEG, мне приходилось конвертировать его в PNG, удалять фон, что тоже было хлопотно, потому что многие инструменты на базе ИИ оставляют артефакты. Но на этом пляски с бубном не заканчивались. Теперь мне нужно было переименовывать загруженные изображения, чтобы избежать написания чрезвычайно длинных путей для каждого файла. А копирование и перемещение вещей в проводнике Windows 7 было отдельной получасовой историей. Там не было нормального Drag and Drop; приходилось либо вырезать, либо копировать папку проекта и ждать, пока всё перезапишется. Мне всё это ужасно надоело, и я решил написать свою собственную небольшую программу, где можно было бы быстро перемещать объекты через командную строку.

# EN 🇬🇧:
## YellowPather version 1.0.4 "The Yellow Brick Road"

Dear Windows 7 nostalgics! Today I want to present my first truly complex project: a file manager (explorer) that I wrote in just 2-3 months, using simple libraries like Tkinter, Pathlib, Platform, and others, as well as my own protection system YPACMv1 (YellowPather Access Control Manager version 1), formerly known as MDEFS. The project repository is available at the link: https://github.com/YarosIshkov2005/YellowPather.git

📑 This is an Open Source project, so everyone can make their own changes, improvements, fixes, etc. Yaroslav Ishkov 2026 ❤️

🔮 What's new in version 1.0.4:
> settings: added the ability to enable/disable the insertion of the selected object's name (does not work when moving from a folder to a folder. Will be fixed in version 1.0.5).

> recursive search: fixed an issue with the create button (the button is disabled during a recursive search).

---

## Section 1: Description 📄

### What is this program 🖥

In this project, I tried to create a simple file explorer for Windows 7, which includes the following features:

**1. Recursive search by extension**

*   `r_*.extension` - (glob) searches for files with the specified extension in the current directory.
*   `r_**.extension` - (rglob) recursively traverses the directory tree, returning files from the current location to the endpoints.

**Command syntax:**

*   `c:\Users\Username\folder\r_*.py` - for Windows.
*   `/home/users/username/folder/r_*.py` - for MacOS/Linux.
    *   `c:\Users\Username\` - the root directory of the device's file system.
    *   `folder\` - the current directory.
    *   `r_*.py` - where `r_*` is the command name, `.py` is the search pattern.

> **Note:** Files are available for superficial viewing only. Opening/modifying files is blocked by default in YellowPather to protect system resources from external interference. This protection applies to all search types (starting from version 1.0.3, you can disable protection in the settings by clicking the Changed button).

> Look for the image with the result in the folder: `YellowPather/Screenshots/`.

**2. Command Line Mode**

In addition to recursive search, YellowPather has a built-in command line mode. To activate it, follow these steps:

**Activation:** Enter the following command in the input field:

*   `c:\Users\Username\cmd-parser:on` - Windows.
*   `/home/users/username/cmd-parser:on` - MacOS/Linux.

> **Purpose:** `cmd-parser:on` activates the command line mode. After this, the input field should display:
> `cmd:/`
> `cmd:/` is the prefix signaling successful command line activation.

**Commands:** Currently, only 3 commands are available (more are planned in the future). Let's look at the syntax for each:

*   `copy "source" to "destination"`
    *   **What it does:** Copies the "source" object to the "destination" folder, where "source" is the path to the object being copied, and "destination" is the path to the target folder.
*   `move "source" to "destination"`
    *   **What it does:** Moves the "source" object to the "destination" folder.
*   `rename "source" to "destination"`
    *   **What it does:** Renames the current name of the "source" object to the new name "destination". For example:
        *   `rename "music" to "Music"` = `music` —> `Music`

**Deactivation:** To return to normal mode, enter the reverse command:
*   `cmd-parser:off`

> **Limitations:**
>
> *   **Objects:** Since the command parser does not support lists of paths, operations can only be performed on a single object in one directory.
> *   **Protection:** The same protection as for recursive search applies in command line mode.
> *   **Case Sensitivity:** The keywords: `copy`, `move`, `rename`, `to` must be specified only in lowercase.
> *   **Workaround:** If the object name contains spaces, enclose the name in single or double quotes, or try working with other objects.

**3. Custom Workspaces 📁**

YellowPather provides 2 access levels:

*   **System Access:**
    *   📁 `c:\Users\Username\` - Windows.
    *   📁 `/home/users/username/` - MacOS/Linux.
*   **Internal Access (chroot):**
    *   📁 `YellowPather/YellowPather/users/0/`

**Switching between zones:**
To switch to internal access, you need to follow these steps:

**Activation:** Open the configuration file:
`YellowPather/YellowPather/config/system_paths.json`

> **Purpose:** `system_paths.json` provides the user access to all access levels through special flags, which we will now look at:
>
> *   `auto_detect`: (Level 1) Automatically determines the path to the root directory based on system data. Disabled by default. When enabled, other flags are ignored.
> *   `root_path`: (Level 1) Works almost the same as `auto_detect`. Its difference is that it determines the path to the root directory based on the OS kernel name, unlike `auto_detect`, which uses a more complex detection algorithm. Disabled by default.
> *   `user_path`: (Level 2) Moves the user to the internal `users/0/` folder, which is an isolated user sandbox. Disabled by default.
>     *   **Alternative:** Disable all flags; Level 2 will be activated automatically.
> *   `device_path`: (Level 1) Works similarly to `auto_detect` and `root_path`. Determines the path to the root folder based on the absolute path using `parents`. Enabled by default.

> There is also a manual input mode. To activate it, disable `auto_detect`, enable `root_path`, `user_path`, `device_path`, click OK in the popup window (this is a reminder to disable the parameters). Enter the path to internal or external storage (SD card or USB).

> **Limitations:** Since `users/0/` is an isolated folder, the user does not have access to the `users/` folder and higher-level folders due to Jail protection (isolation).

---

## Section 2: Technical Specifications ⚙️

**1. Supported OS:**

*   🖥 Windows
*   🖥 MacOS
*   🖥 Linux
*   📱 Android (requires Pydroid 3)

**2. Unsupported OS:**

*   📱 IOS (no native Python support)

**3. Interaction with Device and OS:**

*   **Level 1 (Direct Access):** The main way the program interacts with the device's system. At this level, YellowPather uses standard Python libraries without additional security checks. Most modules and utilities operate at this level.
*   **Level 2 (YPACM):** A more secure method, as it uses security checks based on OS data. Used for tasks requiring careful execution, such as creating a new directory/file, sorting objects. In this case, a `bootstrap()` call from YPACM is used. YPACM also launches a background daemon window to display errors or notifications that require launching from a separate parent window.

P.S.: I don't know why you might need this information, but let's leave it for aesthetics 🤣

**4. Errors and Solutions:**

*   There may be minor bugs or errors in the program, so be prepared for unpredictable behavior in certain scenarios. I will try to fix them in future versions.

**5. Dependencies:**

*   🐍 Python 3.8.10 +
*   🖼 Pillow 12.1.0
*   🖥 charset-normalizer 3.4.4

P.S. Dependencies can be installed with one command: `pip install -r requirement.txt`

---

## Section 3: Launch ✈️

1.  Open an IDE (Integrated Development Environment).
2.  If you are using VSCode, follow these steps:
    *   Go to the **Get Started** tab (usually opens on startup if a project is not already open).
    *   Select the **Open Folder** option (you can also use **Open Editors**).
3.  In the window that opens, click on the folder named `YellowPather`, then select it (VSCode will automatically open the folder).
4.  Select the file named `main.py`.
5.  Run the file in the editor.

P.S.: If you wish, you can also add YellowPather to your desktop by packaging the program into an `.exe` file for Windows or an `.app` file for MacOS and Linux.

**Warning:** Do not use Pyinstaller to package YellowPather! The problem is that Pyinstaller packages the program entirely into a single file, which will prevent the user from accessing user settings (`system_paths.json, settings.json`), as well as isolated sandboxes (`users/0/`), etc.

**Solution:** Use a packager with the ability to manage program resources, for example: `cx_Freeze`.

---

## Section 4: History 📕

...Once, in early December last year, I was writing one of my numerous projects — a music player. Actually, it wasn't entirely my project; I found it on some website. After studying the code, I decided to rewrite it into a more functional state, because the original code was, let's say, subpar. Without thinking twice, I started rewriting the code, and when it came to adding icons for buttons, as well as background GIF animation, minor problems began. To add even one icon, I first had to open the browser, enter a query in the search field, then endlessly scroll through images, and there was no guarantee that a suitable image would be in PNG format and without a background; mostly they were JPEGs. But that wasn't all. If I found a JPEG, I had to convert it to PNG, remove the background, which was also troublesome because many AI-based tools leave artifacts. But the dancing with a tambourine didn't end there. Now I needed to rename the downloaded images to avoid writing extremely long paths for each file. And copying and moving things in Windows 7 Explorer was a separate half-hour story. There was no proper Drag and Drop; you either had to cut or copy the project folder and wait for everything to overwrite. I got terribly tired of all this, and I decided to write my own small program where I could quickly move objects via the command line.