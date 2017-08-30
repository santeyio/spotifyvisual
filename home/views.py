# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import randint

from django.shortcuts import render, redirect
from django.utils.http import urlencode
import requests

from spotifyvisual.private import spotify_keys


CLIENT_ID = spotify_keys['CLIENT_ID']
CLIENT_SECRET = spotify_keys['CLIENT_SECRET']
REDIRECT_URI = 'http://localhost:8000/callback'


def index(request):
    context = {}
    return render(request, 'home/index.html', context)

def login(request):
    state = generate_random_string(16)
    state_key = 'spotify_auth_state'
    scope = 'user-read-private user-read-email'
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
        res = redirect('/callback#' + urlencode({'error': 'state_mismatch'}))
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
            res = requests.get('https://api.spotify.com/v1/me',
                             headers={
                                 'Authorization': 'Bearer ' + access_token,
                                 'Content-Type': 'application/json'})
            return redirect('/callback#' +
                            urlencode({
                                'access_token': access_token,
                                'refresh_token': r_token}))
        else:
            return redirect('/callback#' + urlencode({'error': 'invalid_token'}))

    context = {}
    return render(request, 'home/login.html', context)

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
