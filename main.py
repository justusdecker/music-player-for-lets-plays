import pygame as pg
import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread
from tkinter.filedialog import askdirectory, askopenfilenames, askopenfilename, asksaveasfilename
from json import load, dumps, JSONDecodeError
from tkinter.messagebox import showerror
from random import choice
import os
pg.mixer.init()

"""
+ Deleting Tracks from playlist
* Fix crash issues after deleting track and or issues after importing and reloading
* Block importing, load, save etc. while thread is alive
"""




GRID = 0x0
PACK = 0x1

def btn_crt(master: tk.Widget, text: str = '', command = lambda:print('This btn has no command'),method: int = PACK, options: dict = {}) -> ttk.Button:
    widget = ttk.Button(master,text=text,command=command,style='DM.TButton')
    widget.pack(**options)
    return widget

def slr_crt(master: tk.Widget, method: int = PACK, options: dict = {}) -> tuple[ttk.Scale, tk.DoubleVar]:
    var = tk.DoubleVar(value=0.5)
    widget = ttk.Scale(master,value=0.5,from_=0,to=1.,variable=var)
    widget.pack(**options)
    
    return widget, var
    
def tw_crt(master: tk.Widget,method: int = PACK, options: dict = {}) -> ttk.Treeview:
    widget = ttk.Treeview(master,columns=1, show='headings')
    widget.pack(**options, fill=tk.BOTH)
    return widget

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        
        self.playlist: list[str] = []
        self.is_loop = False
        self.is_shuffle = False
        self.is_playing = False
        self.playlist_loaded = False
        self.is_playing_thread_alive = False
        self.track_path: str = ''
        self.next_interrupt = False
        
        self.title('LetsPlayMediaPlayer')
        self.geometry('600x300')
        
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.plmenu = tk.Menu(self.menu,tearoff=0)
        self.iemenu = tk.Menu(self.menu,tearoff=0)
        
        #+ Load PL, Save PL, Import Files, Import Folder
        self.plmenu.add_command(label='Load',command=self.load_playlist)
        self.plmenu.add_command(label='Save',command=self.save_playlist)
        self.menu.add_cascade(label='Playlist',menu=self.plmenu)

        self.menu.add_cascade(label='Import',menu=self.iemenu)
        self.iemenu.add_command(label='Files',command=self.load_files)
        self.iemenu.add_command(label='Folder',command=self.load_folder)
        
        controls = tk.Frame(self)
        controls.pack()
        self.btn_play_toggle = btn_crt(
            controls,
            'Play',
            self.__toggle_play,
            options={'side':'top'}
        )
        
        self.slr_volume, self.var_volume = slr_crt(controls,options={'side':'top'})
        self.slr_volume.bind('<B1-Motion>',lambda e: pg.mixer_music.set_volume(self.var_volume.get()))

        
        self.btn_loop_toggle = btn_crt(
            controls,
            'Loop',
            self.__toggle_loop,
            options={'side':'left'}
        )
        
        self.btn_shuffle_toggle = btn_crt(
            controls,
            'Shuffle',
            self.__toggle_shuffle,
            options={'side':'left'}
        )
        
        self.btn_shuffle_toggle = btn_crt(
            controls,
            'Next',
            self.__next_track,
            options={'side':'left'}
        )
        
        
        self.create_music_list()

    def set_menu_state(self,state: str = 'disabled'):
        for o,e in [(self.plmenu,0), (self.plmenu,1), (self.iemenu,0), (self.iemenu,1)]: o.entryconfig(e, state=[state])
    
    def toggle_play(self):
        # Verbleibe hier bis Loop deaktiviert oder is_playing false
        if self.is_playing_thread_alive: 
            self.is_playing = False
            return
        if not self.track_path: return
        
        
        self.set_menu_state('disabled')
        
        
        self.is_playing_thread_alive = True
        self.is_playing = True
        self.btn_play_toggle.configure(text = 'Stop')
        while self.is_playing:
            self.title(f'LetsPlayMediaPlayer - {self.track_path}')
            if not self.track_path: return
            pg.mixer_music.load(self.track_path)
            pg.mixer_music.play()
            while pg.mixer_music.get_busy() and self.is_playing:
                if self.next_interrupt:
                    break
            if self.next_interrupt:
                self.next_track()
            self.next_interrupt = False
            pg.mixer_music.unload()
            
            

        self.btn_play_toggle.configure(text = 'Play')
        self.is_playing_thread_alive = False

        self.set_menu_state('active')
        
    def __next_track(self, *_):
        self.next_interrupt = True
        
    def next_track(self):
        
        if self.is_shuffle:
            if not self.playlist:
                self.track_path = ''
                return
            self.track_path = choice(self.playlist)
        elif self.is_loop:
            pass
        else:
            if self.track_path not in self.playlist:
                index = 0
            if not self.playlist:
                self.track_path = ''
                return
            index = self.playlist.index(self.track_path) + 1
            if len(self.playlist) <= index:
                index = 0
            self.track_path = self.playlist[index]
        
    def load_playlist(self,*_):
        """
        Loads the JSON Format Playlist & checks for errors.
        """
        filepath = askopenfilename(filetypes=[('JSON','*.json')])
        if not filepath: return
        self.is_playing = False
        self.playlist = []
        
        try:
            with open(filepath) as f:

                l = load(f)
                if not isinstance(l, list):
                    raise TypeError('Type match failed: <List> in Filepaths')
                for e in l:
                    if not isinstance(e, str):
                        raise TypeError('Type match failed: <List<Str>> in Filepaths')
                    self.playlist.append(e)
                self.__remove_duplicates()
                
            self.create_music_list()
        except JSONDecodeError:
            showerror(message='Playlist Data corrupted')
        except FileNotFoundError:
            showerror(message='File does not exist')
        except OSError:
            showerror(message='The file is not accessible')
        except TypeError:
            showerror(message='Wrong Playlist Format')
            
    def save_playlist(self, *_):
        """
        Saves the playlist in JSON Format.
        """
        filepath = asksaveasfilename(defaultextension='.json',filetypes=[('JSON','*.json')])
        if not filepath: return
        with open(filepath, 'w') as f:
            f.write(dumps(self.playlist))
            
    def load_files(self,*_):
        """
        Extends the Playlist with all the files selected. Only Mp3 allowed
        """
        filepaths = askopenfilenames(filetypes=[('MP3','*.mp3')])
        if not filepaths: return
        self.is_playing = False
        self.playlist.extend(list(filepaths))
        self.__remove_duplicates()
        self.create_music_list()
        
    def load_folder(self,*_):
        """
        Extends the Playlist with all the files in the selected folder, if its a mp3 file
        """
        folderpath = askdirectory()
        if not folderpath: return
        self.playlist.extend([folderpath + '/' + f for f in os.listdir(folderpath) if f.endswith('.mp3')])
        self.__remove_duplicates()
        self.create_music_list()
    
    def create_music_list(self):
        """
        Recreates the music picker element each time the user updates the `self.playlist`
        """
        if hasattr(self,'music_list'):
            self.music_list.destroy()
            
        self.music_list = tw_crt(self)
        for i in self.playlist:
            self.music_list.insert('',0,values=(i,))
        self.music_list.bind('<<TreeviewSelect>>',self.__item_select)
        self.music_list.bind('<Delete>',self.__item_delete)
    
    def __item_delete(self,*_):
        for track in self.music_list.selection():
            value = self.music_list.item(track)['values'][0]
            if value in self.playlist:
                self.playlist.remove(value)
        self.create_music_list()
    
    def __item_select(self,*_):
        if len(self.music_list.selection()) > 1:
            self.music_list.selection_clear()
            return
        self.is_playing = False
        self.track_path = ' '.join(self.music_list.item(self.music_list.selection()[0])['values'])
        self.__toggle_play()
    
    def __toggle_play(self,*_):
        Thread(target=self.toggle_play).start()
        
    def __toggle_shuffle(self, *_):
        self.is_shuffle = not self.is_shuffle
    
    def __toggle_loop(self, *_):
        self.is_loop = not self.is_loop
    
    def __remove_duplicates(self):
        self.playlist = list(set(self.playlist))
    
    def __build_html(self,*_):
        """
        
        """
        ...
if __name__ == '__main__':
    APP = Application()
    APP.mainloop()
        