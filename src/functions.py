from pytubefix import YouTube, Playlist, Channel, Search
from pytubefix.contrib.search import Filter
from pytubefix.cli import on_progress
import pygame
import os
import subprocess

import globals as gl
import messages as ms

# COMMONS
CURRENT_SONG_PATH = None

def play_audio(SONG_NAME_P, PAGE_P):
    global CURRENT_SONG_PATH

    pygame.mixer.init()

    # REMOVE OS CARACTERES '|' E ':' POIS ARQUIVOS ESTES SIMBOLOS QUANDO SALVOS SÃO IGNORADOS.
    song_name = sanitize_filename(SONG_NAME_P)
    song_path = os.path.join(gl.DOWNLOAD_PATH_P, song_name + gl.SONG_FORMAT_P)

    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        CURRENT_SONG_PATH = song_path
    except:
        PAGE_P.open(ms.AD_CANT_PLAY_PAUSE_SOUND_NOT_DOWNLOADED_HOME_M)

def stop_audio(SONG_NAME_P, PAGE_P):
    global CURRENT_SONG_PATH

    pygame.mixer.init()

    # REMOVE OS CARACTERES '|' E ':' POIS ARQUIVOS ESTES SIMBOLOS QUANDO SALVOS SÃO IGNORADOS.
    song_name = sanitize_filename(SONG_NAME_P)
    song_path = os.path.join(gl.DOWNLOAD_PATH_P, song_name + gl.SONG_FORMAT_P)

    if pygame.mixer.music.get_busy():
        # CASO FOR A MUSICA CORRETA
        if CURRENT_SONG_PATH == song_path:
            pygame.mixer.music.pause()
            return

    # CASO SEJA A MUSICA ERRADA
    PAGE_P.open(ms.AD_CANT_PLAY_PAUSE_SOUND_NOT_DOWNLOADED_HOME_M)
    

def sanitize_filename(SONG_NAME_P: str) -> str:
    return " ".join(SONG_NAME_P.replace("|", "").replace(":", "").split())

def download(KIND_P, VIDEO_URL_P, title=None, artist=None):
    url = VIDEO_URL_P
    yt = YouTube(url, on_progress_callback=on_progress)

    if KIND_P == "AUDIO":
        ys = yt.streams.get_audio_only()
    elif KIND_P == "VIDEO":
        ys = yt.streams.get_highest_resolution()

    file_path = ys.download(output_path=gl.DOWNLOAD_PATH_P)
    
    if KIND_P == "AUDIO" and file_path.endswith('.m4a') and title and artist:
        new_filename = f"{sanitize_filename(title)} - {sanitize_filename(artist)}" + gl.SONG_FORMAT_P
        new_file_path = os.path.join(gl.DOWNLOAD_PATH_P, new_filename)
        new_file_path = " ".join(new_file_path.split())
        
        # PRECISA DO ffmpeg NA VARIAVEL PATH.
        cmd = f'ffmpeg -i "{file_path}" -b:a 192K "{new_file_path}" -y'
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        os.remove(file_path)

def download_playlist(KIND_P, VIDEO_URL_P):
    url = VIDEO_URL_P

    pl = Playlist(url)
    for video in pl.videos:
        if KIND_P == "AUDIO":
            ys = video.streams.get_audio_only()
        if KIND_P == "VIDEO":
            ys = video.streams.get_highest_resolution()
        ys.download()

def use_OAuth(KIND_P, VIDEO_URL_P):
    url = VIDEO_URL_P

    yt = YouTube(url, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress)
    if KIND_P == "AUDIO":
        ys = yt.streams.get_audio_only()
    if KIND_P == "VIDEO":
        ys = yt.streams.get_highest_resolution()
    ys.download()


# USING SUBTITLES/CAPTION TRACKS
def view_subtitles(VIDEO_URL_P):
    yt = YouTube(VIDEO_URL_P)
    print(yt.captions)

def view_subtitles_track(VIDEO_URL_P):
    yt = YouTube(VIDEO_URL_P)
    caption = yt.captions['a.en']
    print(caption.generate_srt_captions())

def save_subtitles_textfile(VIDEO_URL_P):
    yt = YouTube(VIDEO_URL_P)
    caption = yt.captions['a.en']
    caption.save_captions("captions.txt")


# SEARCH CHANNEL
def get_channel_name(CHANNEL_LINK_P):
    c = Channel(CHANNEL_LINK_P)
    print(f'Channel name: {c.channel_name}')

def download_all_channel_videos(CHANNEL_LINK_P):
    c = Channel(CHANNEL_LINK_P)
    print(f'Downloading videos by: {c.channel_name}')

    for video in c.videos:
        video.streams.get_highest_resolution().download()


# SEARCH VIDEOS
def basic_search(VIDEO_TITLE_P):
    results = Search(VIDEO_TITLE_P)
    videos = []
    for video in results.videos:
        videos.append({
            "title": video.title,
            "artist": video.author,
            "duration": video.length,
            "url": video.watch_url
        })
    return videos

def use_filters(UPLOAD_DATE_P, TYPE_P, DURATION_P, FEATURE_P, SORT_BY, SEARCH_P):
    filters = {
        'upload_date': Filter.get_upload_date(UPLOAD_DATE_P),
        'type': Filter.get_type(TYPE_P),
        'duration': Filter.get_duration(DURATION_P),
        'features': [Filter.get_features(FEATURE_P)],
        'sort_by': Filter.get_sort_by(SORT_BY)
    }

    s = Search(SEARCH_P, filters=filters)
    for video in s.videos:
        print(video.title + " - " + video.watch_url)
