import pygame as pg
import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread
import os
pg.mixer.init()
P = 'E:/musik/sortiert/Nightcore/'
TRACKS = [P + t for t in os.listdir(P)]

GRID = 0x0
PACK = 0x1

def btn_crt(master: tk.Widget, text: str = '', command = lambda:print('This btn has no command'),method: int = PACK, options: dict = {}) -> ttk.Button:
    widget = ttk.Button(master,text=text,command=command)
    widget.pack(*options)
    return widget
    
def tw_crt(master: tk.Widget,method: int = PACK, options: dict = {}) -> ttk.Treeview:
    widget = ttk.Treeview(master,columns=['Tracks'], show='headings')
    widget.pack(*options)
    return widget

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.is_playing = False
        self.playlist_loaded = False
        self.track_path = 'track.mp3'
        self.title('LetsPlayMediaPlayer - LPMP Prototype')
        self.geometry('600x300')
        
        self.music_list = tw_crt(self)
        for i in TRACKS:
            self.music_list.insert('',0,values=i)
        self.music_list.bind('<<TreeviewSelect>>',self.__item_select)
        self.btn_play_toggle = btn_crt(
            self,
            'Play',
            self.__toggle_play
        )
        
    def __item_select(self,*_):
        if len(self.music_list.selection()) > 1:
            self.music_list.selection_clear()
            return
        print(self.music_list.item(self.music_list.selection()[0]))
        
        self.track_path = ' '.join(self.music_list.item(self.music_list.selection()[0])['values'])
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
        