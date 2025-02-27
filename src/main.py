import flet as ft
import os
import pygame

import functions as fn
import globals as gl
import messages as ms

import songs_screen

def main_screen(page: ft.Page):
    main(page)

def main(page: ft.Page):
    page.title = "Salamander Songs - Home"
    
    songs_button = ft.ElevatedButton(" ", 
                                     icon=ft.Icons.MUSIC_NOTE, 
                                     tooltip="Open My Songs Gallery", 
                                     style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),),
                                     on_click=lambda e: (page.clean(), 
                                                         songs_screen.songs_screen(page, 
                                                                                   main_screen)))
    search_bar = ft.TextField(label="Song Name", 
                              expand=True)
    search_button = ft.ElevatedButton(" ", 
                                      icon=ft.Icons.SEARCH, 
                                      tooltip="Search for a music by name", 
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),),
                                      on_click=lambda e: search_music())
    loading_indicator = ft.ProgressBar(visible=False)
    download_indicator = ft.ProgressBar(visible=False)

    results_container = ft.Container(
        content=ft.Column(scroll=ft.ScrollMode.AUTO),
        height=600,
    )

    videos = []

    def search_music():
        nonlocal videos
        results_container.content.controls.clear()
        query = search_bar.value.strip()
        if query:
            loading_indicator.visible = True
            page.update()

            videos = fn.basic_search(query)
            loading_indicator.visible = False
            page.update()

            for video in videos:
                item_controls = create_video_row(video)
                results_container.content.controls.append(item_controls)

        page.update()

    def delete_song(title, artist):
        filename = f"{fn.sanitize_filename(title)} - {fn.sanitize_filename(artist)}" + gl.SONG_FORMAT_P
        file_path = os.path.join(gl.DOWNLOAD_PATH_P, filename)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)

                for item in results_container.content.controls:
                    if (len(item.controls) >= 3 and 
                        isinstance(item.controls[1], ft.Text) and 
                        item.controls[1].value == title and 
                        item.controls[2].value == artist):
                        if isinstance(item.controls[0], ft.Icon):
                            item.controls.pop(0)
                        break
            else:
                # CASO A MUSICA NÃO ESTEJA BAIXADA
                page.open(ms.AD_CANT_DELETE_SOUND_PLAYING_HOME_M)
        except PermissionError:
            page.open(ms.AD_CANNOT_DELETE_LAST_AUDIO_USED_M)

        page.update()

    def create_video_row(video):
        filename = f"{fn.sanitize_filename(video['title'])} - {fn.sanitize_filename(video['artist'])}" + gl.SONG_FORMAT_P
        audio_file_path = os.path.join(gl.DOWNLOAD_PATH_P, filename)

        item_controls = [
            ft.Text(video["title"], 
                    weight=ft.FontWeight.BOLD),
            ft.Text(video["artist"]),
            ft.Text(f'{video["duration"] // 60}:{video["duration"] % 60:02d}'),
            ft.ElevatedButton(" ", 
                              icon=ft.Icons.DOWNLOAD, 
                              tooltip="Download this song", 
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),), 
                              on_click=lambda e, 
                              title=video["title"], 
                              artist=video["artist"], 
                              url=video["url"]: download_music(title, 
                                                               artist, 
                                                               url)),
            ft.ElevatedButton(" ", 
                              icon=ft.Icons.PLAY_ARROW, 
                              tooltip="Play this song", 
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),), 
                              on_click=lambda e, 
                              title=video["title"], 
                              artist=video["artist"]: fn.play_audio(f"{fn.sanitize_filename(title)} - {fn.sanitize_filename(artist)}", 
                                                                    page)),
            ft.ElevatedButton(" ", 
                              icon=ft.Icons.PAUSE, 
                              tooltip="Pause this song", 
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),),
                              on_click=lambda e, 
                              title=video["title"], 
                              artist=video["artist"]: fn.stop_audio(f"{fn.sanitize_filename(title)} - {fn.sanitize_filename(artist)}", 
                                                                    page)),
            ft.ElevatedButton(" ", 
                              icon=ft.Icons.DELETE, 
                              tooltip="Delete this Song", 
                              icon_color="red",
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),), 
                              on_click=lambda e, 
                              title=video["title"], 
                              artist=video["artist"]: delete_song(title, 
                                                                  artist))
        ]

        if os.path.isfile(audio_file_path):
            item_controls.insert(0, 
                                 ft.Icon(ft.icons.CHECK_CIRCLE, 
                                         color=ft.colors.GREEN))

        return ft.Row(item_controls)

    def download_music(title, artist, url):
        download_indicator.visible = True
        page.update()

        fn.download("AUDIO", 
                    url, 
                    title, 
                    artist)

        download_indicator.visible = False
        page.update()

        for item in results_container.content.controls:
            title_text = None
            artist_text = None
            if len(item.controls) >= 3:
                if isinstance(item.controls[0], ft.Icon):
                    if isinstance(item.controls[1], ft.Text):
                        title_text = item.controls[1].value
                    if len(item.controls) >= 4 and isinstance(item.controls[2], ft.Text):
                        artist_text = item.controls[2].value
                else:
                    if isinstance(item.controls[0], ft.Text):
                        title_text = item.controls[0].value
                    if len(item.controls) >= 2 and isinstance(item.controls[1], ft.Text):
                        artist_text = item.controls[1].value

                if title_text == title and artist_text == artist:
                    if not isinstance(item.controls[0], ft.Icon):
                        item.controls.insert(0, 
                                             ft.Icon(ft.Icons.CHECK_CIRCLE, 
                                                     color=ft.Colors.GREEN))
                    break

        page.update()

    page.add(ft.Row([songs_button, 
                     search_bar, 
                     search_button]), 
             loading_indicator, 
             download_indicator, 
             results_container)

ft.app(target=main)
