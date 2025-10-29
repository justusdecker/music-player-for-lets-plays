![ICO](MPLP.png)

# 🎧 LetsPlayMediaPlayer

A simple **MP3 media player** with a graphical user interface (GUI), built using **Tkinter** for the interface and the **pygame** library for audio playback.

## 🌟 Core Functionality

A simple, feature-rich media player specifically designed for use during live streams or recording **Lets Plays**. It allows for the management of music playlists and the optional export of the currently playing title to an HTML file.

## ✨ Features

* **GUI Playlist Management:** Add individual MP3 files or entire folders.
* **Playlist Saving:** Save and load playlists in **JSON format**.
* **Playback Controls:**
    * Start/Stop playback.
    * **Shuffle** playback.
    * Skip to the **next** track.
    * Volume control.
* **HTML Export:** Exports the current song title and artist to a separate `export.html` file. Ideal for displaying as a browser source in streaming software (like OBS Studio) to inform viewers.
* **Native Interface:** Uses `tkinter` for a simple and cross-platform user interface.
* **Delete Tracks** directly from the playlist view (via the `Delete` key).

## 🛠️ How to

### Executable

If you are using the provided **executable file**, no installation is required—simply run the application.

### Building from Source (Optional)

If you are building the application from the source code, you must install the required dependencies first:

1.  Make sure you have Python 3 installed.
2.  Install the necessary libraries from the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

3.  Run the application:

    ```bash
    python player.py
    ```

### Using the HTML Export

The application automatically generates a file named `export.html` in the same directory. This file contains the formatted title of the currently playing song.

* **Song Title Convention:** The `__build_html` function expects your filenames to be in the format `Artist - Title.mp3` to correctly split and display the artist and title.
* **Streaming Setup:** Add this `export.html` to your streaming software as a **"Browser Source"**.

---

## 🏗️ Technical Overview

The player is structured within a single **`Application(tk.Tk)`** class.

| Component | Purpose | Libraries |
| :--- | :--- | :--- |
| **GUI** | Main window, menus, buttons, slider, and playlist list (`Treeview`). | `tkinter`, `tkinter.ttk` |
| **Audio Playback** | Loading and playing MP3 files, volume control. | `pygame.mixer` |
| **Background Process**| Non-blocking, continuous playlist playback and track switching logic. | `threading.Thread` |
| **HTML Export** | Generation of `export.html` for displaying the current title. | `os` |

---

## 📄 License

This project is licensed under the following license: GPL-V3