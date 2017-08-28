# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'home/index.html', context)

def callback(request):
    context = {}
    return render(request, 'home/callback.html', context)

def login(request):
    context = {}
    return render(request, 'home/login.html', context)
