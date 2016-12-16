# -*- coding: utf-8 -*-
import re
import time
import sys
import vk_requests
from login import login, password, app_id
api = vk_requests.create_api(app_id=app_id, login=login, password=password, scope=['audio', 'status'])


if sys.platform == "win32":
    import win32gui
elif sys.platform == "darwin":
    import subprocess
else:
    import subprocess
    import dbus


def getwindowtitle():
    if sys.platform == "win32":
        spotify = win32gui.FindWindow('SpotifyMainWindow', None)
        windowname = win32gui.GetWindowText(spotify)
    elif sys.platform == "darwin":
        windowname = ''
        try:
            command = "osascript getCurrentSong.AppleScript"
            windowname = subprocess.check_output(["/bin/bash", "-c", command]).decode("utf-8")
        except Exception:
            pass
    else:
        windowname = ''
        session = dbus.SessionBus()
        spotifydbus = session.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
        spotifyinterface = dbus.Interface(spotifydbus, "org.freedesktop.DBus.Properties")
        metadata = spotifyinterface.Get("org.mpris.MediaPlayer2.Player", "Metadata")
        try:
            command = "xwininfo -tree -root"
            windows = subprocess.check_output(["/bin/bash", "-c", command]).decode("utf-8")
            spotify = ''
            for line in windows.splitlines():
                if '("spotify" "Spotify")' in line:
                    if " - " in line:
                        spotify = line
                        break
            if spotify == '':
                windowname = 'Spotify'
        except Exception:
            pass
        if windowname != 'Spotify':
            windowname = "%s - %s" % (metadata['xesam:artist'][0], metadata['xesam:title'])
    if "—" in windowname:
        windowname = windowname.replace("—", "-")
    if "Spotify - " in windowname:
        windowname = windowname.strip("Spotify - ")
    return windowname


def main():
    oldsongname = ""
    while True:
        songname = getwindowtitle()
        if oldsongname != songname and songname != "Spotify":
            oldsongname = songname
            print(songname)
            query = re.sub("[(\[].*?[)\]]", "", songname)
            print(query)
            top_search = api.audio.search(q='{}'.format(query), sort=2, count=10)
            print(top_search)
            try:
                owner_audio = '{}_{}'.format(top_search['items'][0]['owner_id'], top_search['items'][0]['id'])
                print(owner_audio)
                sets = api.audio.setBroadcast(audio=owner_audio)
                print(songname, 'уже в статусе', sets)
            except IndexError:
                print(songname, 'не найдена')
        time.sleep(1)


if __name__ == '__main__':
    main()
