import pygame as pg
import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread
from tkinter.filedialog import askdirectory, askopenfilenames, askopenfilename, asksaveasfilename
from json import load, dumps, JSONDecodeError
from tkinter.messagebox import showerror

import os
pg.mixer.init()

"""
+ Adding tracks to playlist
+ Save playlist
+ Deleting Tracks from playlist
+ Loop
+ Shuffle
+ Next
+ Last

Final:

2 Seperate Functionalitys:
    1. Creating the playlist
    2. play the audio
"""

GRID = 0x0
PACK = 0x1

def btn_crt(master: tk.Widget, text: str = '', command = lambda:print('This btn has no command'),method: int = PACK, options: dict = {}) -> ttk.Button:
    widget = ttk.Button(master,text=text,command=command)
    widget.pack(*options)
    return widget

def slr_crt(master: tk.Widget, method: int = PACK, options: dict = {}) -> tuple[ttk.Scale, tk.DoubleVar]:
    var = tk.DoubleVar()
    widget = ttk.Scale(master,value=0.5,from_=0,to=1.,variable=var)
    widget.pack(*options)
    
    return widget, var
    
def tw_crt(master: tk.Widget,method: int = PACK, options: dict = {}) -> ttk.Treeview:
    widget = ttk.Treeview(master,columns=1, show='headings')
    widget.pack(*options, fill=tk.X)
    return widget

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.playlist: list[str] = []
        
        self.is_playing = False
        self.playlist_loaded = False
        self.track_path = 'track.mp3'
        self.title('LetsPlayMediaPlayer - LPMP Prototype')
        self.geometry('600x300')
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.plmenu = tk.Menu(self.menu,tearoff=0)
        
        #+ Load PL, Save PL, Import Files, Import Folder
        self.plmenu.add_command(label='Load',command=self.load_playlist)
        self.plmenu.add_command(label='Save',command=self.save_playlist)
        self.menu.add_cascade(label='Playlist',menu=self.plmenu)
        
        

        self.iemenu = tk.Menu(self.menu,tearoff=0)
        self.menu.add_cascade(label='Import',menu=self.iemenu)
        self.iemenu.add_command(label='Files',command=self.load_files)
        self.iemenu.add_command(label='Folder',command=self.load_folder)
        
        
        self.btn_play_toggle = btn_crt(
            self,
            'Play',
            self.__toggle_play
        )
        self.slr_volume, self.var_volume = slr_crt(self,)
        self.slr_volume.bind('<B1-Motion>',lambda e: pg.mixer_music.set_volume(self.var_volume.get()))

        self.create_music_list()
        
    def load_playlist(self,*_):
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
        filepath = asksaveasfilename(defaultextension='.json',filetypes=[('JSON','*.json')])
        if not filepath: return
        with open(filepath, 'w') as f:
            f.write(dumps(self.playlist))
            
    def load_files(self,*_):
        filepaths = askopenfilenames(filetypes=[('MP3','*.mp3')])
        if not filepaths: return
        self.is_playing = False
        
        self.playlist.extend(list(filepaths))
        print(self.playlist)
        self.create_music_list()
        
    def load_folder(self,*_):
        folderpath = askdirectory()
        if not folderpath: return
        self.playlist.extend([folderpath + '/' + f for f in os.listdir(folderpath) if f.endswith('.mp3')])
        self.create_music_list()
    
    def create_music_list(self):
        if hasattr(self,'music_list'):
            self.music_list.destroy()
            
        self.music_list = tw_crt(self)
        for i in self.playlist:
            self.music_list.insert('',0,values=(i,))
        self.music_list.bind('<<TreeviewSelect>>',self.__item_select)
        self.music_list.bind('<<Delete>>',self.__item_delete)
    
    def __item_delete(self,*_):
        self.music_list.selection()
    
    def __item_select(self,*_):
        if len(self.music_list.selection()) > 1:
            self.music_list.selection_clear()
            return
        self.is_playing = False
        self.track_path = ' '.join(self.music_list.item(self.music_list.selection()[0])['values'])
        self.__toggle_play()
    def __toggle_play(self,*_):
        Thread(target=self.toggle_play).start()
    def toggle_play(self):
        
        if self.is_playing:
            self.is_playing = False
            self.btn_play_toggle.configure(text = 'Play')
            return
        self.btn_play_toggle.configure(text = 'Stop')
        pg.mixer_music.load(self.track_path)
        pg.mixer_music.play()
        self.is_playing = True
        while pg.mixer_music.get_busy() and self.is_playing:
            pass
        pg.mixer_music.unload()
if __name__ == '__main__':
    APP = Application()
    APP.mainloop()
        