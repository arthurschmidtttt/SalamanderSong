import flet as ft

AD_CANT_DELETE_SOUND_PLAYING_HOME_M = ft.AlertDialog(
        title=ft.Text("You cannot delete a song that has not been downloaded or is not playing!"),
    )

AD_CANT_DELETE_SOUND_PLAYING_MY_SONGS_M = ft.AlertDialog(
        title=ft.Text("You cannot delete a song that has not been downloaded or is currently playing!"),
    )

AD_CANT_PLAY_PAUSE_SOUND_NOT_DOWNLOADED_HOME_M = ft.AlertDialog(
        title=ft.Text("You cannot play a song that has not been downloaded or pause one that is not currently playing!"),
    )

AD_CANNOT_DELETE_LAST_AUDIO_USED_M = ft.AlertDialog(
        title=ft.Text("You cannot delete the last used or currently playing audio!"),
    )
