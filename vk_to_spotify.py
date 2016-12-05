#!/usr/bin/env python3

import vk
import requests
import re


vk_token = input('Введите полученый токен от вк')
spotusy_token = input('Введите полученый токен от spotify')
owner_id = input('Введите идентификатор владельца аудиозаписей: ')
album_id = input('Введите идентификатор альбома с аудиозаписями. По умолчанию - основной ')
offset = input('Введите смещение, необходимое для выборки определенного количества аудиозаписей. По умолчанию - с начала.')
count = input('Введите количество аудиозаписей. По умолчанию все ')
session = vk.Session(access_token=vk_token)
api = vk.API(session, v='5.60', lang='ru')
audio = api.audio.get(owner_id=owner_id, album_id=album_id, offset=offset, count=count)

songs = []
track_ids = []


def get_songs():
    for i in range(len(audio['items'])):
        song = audio['items'][i]['artist'] + ' ' + audio['items'][i]['title']
        songs.append(song)
    return songs

headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(spotusy_token),
}


def get_items():
    for i in get_songs():
        query = re.sub("[(\[].*?[)\]]", "", i)
        url = 'https://api.spotify.com/v1/search?q={}&type=artist,track&limit=1'.format(query.replace(' ', '+'))
        r = requests.get(url, headers=headers)
        jsons = r.json()
        try:
            track_ids.append(jsons['tracks']['items'][0]['uri'][14:])
            print('Песяня ' + i + ' найдена')
        except IndexError:
            print('Песяня ' + i + ' не найдена')
        except KeyError:
            print("Обновите токен спотифай")
            break
    print('Найдено', len(track_ids), 'песен с', len(songs),  'Не найдено: ', len(songs) - len(track_ids))
    return track_ids


def add_to_spotify():
    for track_id in get_items():
        requests.put('https://api.spotify.com/v1/me/tracks?ids={}'.format(track_id), headers=headers)

add_to_spotify()
