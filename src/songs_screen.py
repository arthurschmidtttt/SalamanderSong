import flet as ft
import os

import functions as fn
import globals as gl
import messages as ms

def songs_screen(page: ft.Page, main_screen):
    page.title = "Salamander Songs - My Songs"

    search_bar = ft.TextField(label="Search Song", 
                              expand=True)
    search_button = ft.ElevatedButton(" ", 
                                      icon=ft.Icons.SEARCH, 
                                      tooltip="Search for a music by name", 
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),),
                                      on_click=lambda e: load_songs(search_bar.value))
    back_button = ft.ElevatedButton(" ", 
                                    icon=ft.Icons.HOME, 
                                    tooltip="Return to home", 
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),),
                                    on_click=lambda e: (page.clean(), 
                                                        main_screen(page)))

    song_list = ft.Column(scroll=ft.ScrollMode.AUTO)

    def load_songs(query=""):
        song_list.controls.clear()
        for song in os.listdir(gl.DOWNLOAD_PATH_P):
            if song.endswith(gl.SONG_FORMAT_P):
                if query.lower() in song.lower():
                    song_list.controls.append(create_song_row(song))
        page.update()

    def create_song_row(song):
        base_name = song.replace(gl.SONG_FORMAT_P, "")
        title = song
        
        return ft.Row([
            ft.Text(title),
            ft.ElevatedButton(" ", 
                              icon=ft.Icons.PLAY_ARROW, 
                              tooltip="Play this song", 
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),), 
                              on_click=lambda e: fn.play_audio(base_name, 
                                                               page)),
            ft.ElevatedButton(" ", 
                              icon=ft.Icons.PAUSE, 
                              tooltip="Pause this song", 
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),),
                              on_click=lambda e: fn.stop_audio(base_name, 
                                                               page)),
            ft.ElevatedButton(" ", 
                              icon=ft.Icons.DELETE, 
                              tooltip="Delete this Song", 
                              icon_color="red", 
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),), 
                              on_click=lambda e, 
                              title=title: delete_song(title))
        ])

    def delete_song(title):
        try:
            if os.path.exists(gl.DOWNLOAD_PATH_P + title):
                os.remove(gl.DOWNLOAD_PATH_P + title)
        except PermissionError:
            page.open(ms.AD_CANT_DELETE_SOUND_PLAYING_MY_SONGS_M)
            return
        load_songs()
        
    load_songs()

    page.add(ft.Column([ft.Row([back_button, 
                                search_bar, 
                                search_button]), 
                        song_list]))
