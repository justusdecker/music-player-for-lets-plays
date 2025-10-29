![ICO](MPLP.png)

# 🎧 LetsPlayMediaPlayer

A simple **MP3 media player** with a graphical user interface (GUI), built using **Tkinter** for the interface and the **pygame** library for audio playback.

## 🌟 Core Functionality

LetsPlayMediaPlayer allows users to easily manage and play their MP3 music collection.

* **GUI Operation:** Intuitive graphical user interface based on `tkinter`.
* **Music Playback:** Uses `pygame.mixer` to load, play, pause/stop, and adjust the volume of selected MP3 files. Playback runs in a separate **Thread** (`threading`) to keep the GUI responsive.
* **Playlist Management:**
    * **Import:** Add individual MP3 files or all MP3 files from a selected folder to the playlist.
    * **Save/Load:** Save the current playlist (a list of file paths) in **JSON** format and load it back later.
    * **Duplicate Removal:** Automatically cleans the playlist by removing duplicate entries.
* **Playback Modes:**
    * **Loop:** Toggles continuous playback (currently set up to loop the entire playlist or the current track based on how `next_track` is called in `toggle_play`).
    * **Shuffle:** Randomly selects the next track from the playlist.
* **Track Control:**
    * **Play/Stop:** Toggles the playback state.
    * **Next Track:** Immediately skips to the next title (according to the Loop/Shuffle settings).
    * **Volume Control:** Adjustable volume via a slider widget.
* **Playlist View:** Displays the loaded tracks in a `Treeview` list, where selecting a track immediately starts playback. The code also includes logic for **deleting selected tracks** from the playlist using the delete key (bound to `<Delete>`).

## 🛠️ Dependencies

The program requires the following Python libraries:

* **`pygame`:** For music playback (`pg.mixer`).
* **`tkinter` and `tkinter.ttk`:** For the graphical user interface and widgets.
* **Standard Libraries:** `threading`, `json`, `os`, `random`, `time`.