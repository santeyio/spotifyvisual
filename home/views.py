# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import randint

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.http import urlencode, urlquote
import requests

from spotifyvisual.private import spotify_keys


CLIENT_ID = spotify_keys['CLIENT_ID']
CLIENT_SECRET = spotify_keys['CLIENT_SECRET']
REDIRECT_URI = spotify_keys['REDIRECT_URI']


def index(request):
    context = {}
    return render(request, 'home/index.html', context)

def visualizations(request):
    context = {}
    context['access_token'] = request.GET.get('access_token', False)
    return render(request, 'home/visualizations.html', context)

def song(request):
    name = request.GET.get('name', False)
    artist = request.GET.get('artist', False)
    count = {}
    if name and artist:
        lyrics = get_lyrics(artist, name)
        try:
            count = parse_lyrics(lyrics['lyrics'], count)
        except KeyError:
            return JsonResponse({'error': 'no lyrics found'})
        return JsonResponse(count)


def playlists(request, playlist_id=False):
    access_token = request.COOKIES['access_token'] if request.COOKIES else False
    offset = request.GET.get('offset', 0)
    owner_id = request.GET.get('owner_id', False)
    lyrics = request.GET.get('lyrics', False)
    count = {}
    if playlist_id:
        total = 100
        track_list = []
        no_lyrics = []
        while (offset < total):
            data = get_playlist_from_spotify(owner_id, playlist_id, access_token, offset)
            track_list += format_track_list(data)
            offset += 100
        # print "track list: ", track_list
        if lyrics:
            # for track in track_list:
                # print 'track: ', track
                # lyrics = get_lyrics(track['artist'], track['name'])
                # try:
                    # count = parse_lyrics(lyrics['lyrics'], count)
                # except KeyError:
                    # no_lyrics.append(track)
            lyrics = get_lyrics(track_list[0]['artist'], track_list[0]['name'])
            count = parse_lyrics(lyrics['lyrics'], count)
            print no_lyrics
            return JsonResponse(count)
        else:
            return JsonResponse(track_list, safe=False)
    else:
        res = requests.get(
                'https://api.spotify.com/v1/me/playlists',
                params={
                    'limit': 50,
                    'offset': offset,
                },
                headers={
                    'Authorization': 'Bearer ' + access_token
                }
            )
        return JsonResponse(res.json())

def get_playlist_from_spotify(owner_id, playlist_id, access_token, offset):
    res = requests.get(
        'https://api.spotify.com/v1/users/'+owner_id+'/playlists/'+playlist_id+'/tracks',
        params={
            'limit': 100,
            'offset': offset
        },
        headers={
            'Authorization': 'Bearer ' + access_token
        })
    return res.json()

def format_track_list(track_list_from_spotify):
    formatted_track_list = []
    for track in track_list_from_spotify['items']:
        formatted_track_list.append({
            'artist': track['track']['artists'][0]['name'],
            'name': track['track']['name'],
        })
    return formatted_track_list

def get_lyrics(artist, name):
    res = requests.get('http://api.lyrics.ovh/v1/'+urlquote(artist)+'/'+urlquote(name))
    data = res.json()
    # print data
    return data
    
def parse_lyrics(lyrics, count):
    lyrics = lyrics.split()
    for word in lyrics:
        word = word.lower()
        word = word.rstrip('?:!.,;"\'')
        try:
            count[word] += 1
        except KeyError:
            count[word] = 1
    return count


# --------- Spotify Auth Stuff -------------

def login(request):
    state = generate_random_string(16)
    state_key = 'spotify_auth_state'
    scope = 'user-read-private user-read-email playlist-read-private'
    res = redirect('https://accounts.spotify.com/authorize?' +
                   urlencode({
                       'response_type': 'code',
                       'client_id': CLIENT_ID,
                       'scope': scope,
                       'redirect_uri': REDIRECT_URI,
                       'state': state}))
    res.set_cookie(key=state_key, value=state)
    return res

def callback(request):
    code = request.GET.get('code', False)
    state = request.GET.get('state', False)
    stored_state = request.COOKIES['spotify_auth_state'] if request.COOKIES else False

    if not state or state != stored_state:
        f_res = redirect('/visualizations?' + urlencode({'error': 'state_mismatch'}))
    else:
        res = requests.post(
            'https://accounts.spotify.com/api/token',
            data={
                'code': code,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code'
            },
            headers={
                'Authorization': 'Basic ' + (CLIENT_ID+":"+CLIENT_SECRET)
                                 .encode('base64').replace("\n", "")})

        if res.status_code == 200:
            j = res.json()
            access_token = j['access_token']
            r_token = j['refresh_token']
            f_res = redirect('/visualizations?' +
                            urlencode({
                                'access_token': access_token,
                                'refresh_token': r_token}))
            f_res.set_cookie(key="access_token", value=access_token)
        else:
            f_res = redirect('/visualizations?' + urlencode({'error': 'invalid_token'}))

    return f_res

def refresh_token(request):
    refresh_token = request.GET.get('refresh_token', False)
    res = requests.post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        },
        headers={
            'Authorization': 'Basic ' + (CLIENT_ID+":"+CLIENT_SECRET)
                             .encode('base64').replace("\n", "")})
    if res.status_code == 200:
        access_token = res.json()['access_token']
        # return HttpResponse(json.dumps({'access_token': access_token}))
        return redirect(
            '/login' +
            urlencode({
                'access_token': access_token,
                'refresh_token': refresh_token}))


def generate_random_string(length):
    random_string = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    for i in range(length):
        random_string += possible[randint(0, len(possible)-1)]

    return random_string
