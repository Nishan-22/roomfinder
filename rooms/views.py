from django.shortcuts import render, get_object_or_404
from .models import Room

# SHOW ALL ROOMS
def room_list(request):
    rooms = Room.objects.all().order_by('-created_at')
    return render(request, 'rooms/room_list.html', {'rooms': rooms})


# SHOW SINGLE ROOM
def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    return render(request, 'rooms/room_detail.html', {'room': room})
