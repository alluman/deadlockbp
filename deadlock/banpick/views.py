# views.py

from django.shortcuts import render

def index(request):
    return render(request, 'banpick/index.html')

def room(request, room_name):
    return render(request, 'banpick/banpick.html', {'room_name': room_name})
