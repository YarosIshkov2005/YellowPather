README.md

YellowPather version 1.0.0 "Yellow Brick Road"

Dear Windows 7 nostalgics! Today I'd like to present to you my first truly challenging project: a file manager (explorer) that I wrote in just 2-3 months, using simple libraries such as Tkinter, Pathlib, Platform, etc., as well as my own protection system YPACMv1 (YellowPather Access Control Manager version 1), formerly known as MDEFS. The project repository is available at the link: https://github.com/YarosIshkov2005/YellowPather.git

📑 This is an Open Source project, so everyone can contribute their own changes, improvements, fixes, etc. YarosIshkov 2026 ❤️

---

Section 1: Description 📄

What is the program 🖥

In this project, I attempted to create a simple file explorer for Windows 7, which includes the following features:

1. Recursive Search by Extension

· r_*.extension - (glob) searches for files with the specified extension within the current directory.
· r_**.extension - (rglob) recursively traverses the directory tree, returning files from the current location to the end points.

Command Syntax:

· c:\Users\Username\folder\r_*.py - for Windows.
· /home/users/username/folder/r_*.py - for MacOS/Linux.
  · c:\Users\Username\ - root directory of the device's file system.
  · folder\ - current directory.
  · r_*.py - where r_* is the command name, .py is the search pattern.

» Note: Files are available only for superficial viewing. Opening/modifying files is blocked by default in YellowPather to protect system resources from external interference. This protection applies to all search types.

» Look for the result image in the folder: YellowPather/Screenshots/.

2. Command Line Mode

In addition to recursive search, YellowPather has a built-in command line mode. To activate it, follow these steps:

Activation: Enter the following command in the input field:

· c:\Users\Username\cmd-parser:on - Windows.
· /home/users/username/cmd-parser:on - MacOS/Linux.

» Purpose: cmd-parser:on activates the command line mode. After this, the input field should display:

· cmd:/
  » cmd:/ is the prefix signaling that the command line has been successfully activated.

Commands: Currently, only 3 commands are available (more are planned for the future). Let's look at the syntax for each:

· copy "source" to "destination"
  » What it does: Copies the "source" object to the "destination" folder, where "source" is the path to the object to be copied, and "destination" is the path to the target folder.
· move "source" to "destination"
  » What it does: Moves the "source" object to the "destination" folder.
· rename "source" to "destination"
  » What it does: Renames the current name of the "source" object to the new name "destination". For example:
  · rename "music" to "Music" = music —> Music

Deactivation: To return to normal mode, enter the reverse command:

· cmd-parser:off

» Limitations:

· Objects: Since the command parser does not support lists of paths, operations can only be performed on a single object within the same directory.
· Protection: The same protection as for recursive search applies in command line mode.
· Case Sensitivity: Keywords: copy, move, rename, to must be specified in lowercase only.
· Errors: There is a known issue that occurs during operation execution. This happens because the command parser cannot find one of the specified points in the path_manager.abs_paths list if the path to the source or destination was constructed incorrectly. This issue will be fixed in version 1.0.1.
  » Workaround: If there are spaces in the object name, enclose the name in single or double quotes, or try with other objects. If there are no results, use the standard explorer or another one.

3. User Workspaces 📁

YellowPather provides 2 access levels:

· System Access:
  · 📁 c:\Users\Username\ - Windows.
  · 📁 /home/users/username/ - MacOS/Linux.
· Internal Access (chroot):
  · 📁 YellowPather/YellowPather/users/0/

Switching between zones:
To switch to internal access, you need to perform the following steps:

Activation: Open the configuration file:
YellowPather/YellowPather/config/system_paths.json

» Purpose: system_paths.json gives the user access to all access levels through special flags, which we will examine right now:

· auto_detect: (Level 1) Automatically determines the path to the root directory based on system data. Disabled by default. When enabled, other flags will be ignored.
· root_path: (Level 1) Works almost the same as auto_detect. Its difference is that it determines the path to the root directory based on the OS kernel name, unlike auto_detect, which uses a more complex detection algorithm. Disabled by default.
· user_path: (Level 2) Moves the user to the internal users/0/ folder, which is an isolated user sandbox. Disabled by default.
  » Alternative: Disable all flags; Level 2 will be activated automatically.
· device_path: (Level 1) Works similarly to auto_detect and root_path. Determines the path to the root folder based on the absolute path using parents. Enabled by default.

» There is also a manual input mode. To activate it, disable auto_detect, and enable root_path, user_path, device_path, click OK on the popup (this is a reminder to disable the parameters). Enter the path to internal or external storage (SD Card or USB).

» Limitations: Since users/0/ is an isolated folder, the user does not have access to users/ and higher-level folders, due to Jail protection.

---

Section 2: Technical Specifications ⚙️

1. Supported OS:

· 🖥 Windows
· 🖥 MacOS
· 🖥 Linux
· 📱 Android (requires Pydroid 3)

2. Unsupported OS:

· 📱 IOS (no native Python support)

3. Interaction with Device and OS:

· Level 1 (Direct Access): The primary way the program interacts with the device's system. At this level, YellowPather uses standard Python libraries without additional security checks. Most modules and utilities operate at this level.
· Level 2 (YPACM): A more secure method, as it uses security checks based on OS data. Used for tasks that require caution during execution, such as the process of creating a new directory/file. In this case, a call to bootstrap() from YPACM is used. YPACM also launches a background daemon window to display errors or notifications that require launching from a separate parent window.

P.S.: I don't know why you might need this information, but let's keep it for aesthetics 🤣

4. Errors and Solutions:

· cmd:/ has a known issue related to constructing the absolute path to the source object, which prevents it from being found in the abs_paths list.
  » Solution: Use the system explorer or any other one. The issue will be fixed in version 1.0.1; path construction will be handled through the Pointer class from YPACM.
· rename_window: YellowPather does not have built-in protection against reserved characters like \ / : * ? " < > | when creating new objects.
  » Solution: Be careful when creating a new directory or file. Protection will be added in version 1.0.1.

5. Dependencies:

· 🐍 Python 3.8.10 +
· 🖼 Pillow 12.1.0
· 🖥 charset-normalizer 3.4.4

P.S. Dependencies can be installed with one command: pip install -r requirement.txt

---

Section 3: Launch ✈️

1. Open a code editor (IDE).
2. If you are using VSCode, follow these steps:
   · Go to the Get Started tab (usually opens on startup if no project is open yet).
   · Select the Open Folder/Directory option (you can also use Open Editors).
3. In the window that opens, click on the folder named YellowPather, then select it (VSCode will automatically open the folder).
4. In the opened folder, select the nested folder with the same name (YellowPather).
5. Select the file named main.py.
6. Run the file in the editor.

P.S.: If desired, you can also add YellowPather to your desktop by packaging the program into a .exe file for Windows, or an .app for MacOS and Linux.

Caution: Do not use Pyinstaller to package YellowPather! The problem is that Pyinstaller packages the program entirely into a single file, which will prevent the user from accessing user settings (system_paths.json), as well as access to isolated sandboxes (users/0/), etc.

Solution: Use a packager with the ability to manage program resources, for example: cx_Freeze.

---

Section 4: History 📕

...Once upon a time, in early December of last year, I was writing one of my numerous projects - a music player. Actually, it wasn't entirely my project; I dug it up on some website. After studying the code, I decided to rewrite it into a more functional state, because the original code was... let's say, a C-grade effort. Without thinking twice, I started rewriting the code, and when it came time to add icons for buttons, as well as a background GIF, some small problems started. To add even one icon, I first had to open a browser, type a query into the search field, then endlessly scroll through images, and it wasn't guaranteed that a suitable image would be in PNG format and without a background; they were mostly JPEG. But that wasn't all. If I found a JPEG, I had to convert it to PNG, remove the background, which was also a hassle because many AI tools leave artifacts. But the song and dance didn't end there. Now I had to rename the downloaded images to avoid writing extremely long paths for each file. And copying and moving things in Windows 7 Explorer was a whole separate half-day story. Drag and Drop didn't really exist back then; you either had to cut or copy the project folder and wait for everything to overwrite. I got terribly fed up with all of this, and I decided to write my own small program where I could quickly move objects via the command line.