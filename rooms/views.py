from django.shortcuts import render, get_object_or_404,redirect
from .models import Room
from .forms import RoomForm
from django.contrib.auth.decorators import login_required


# SHOW ALL ROOMS
def room_list(request):
    rooms = Room.objects.all().order_by('-created_at')
    return render(request, 'rooms/room_list.html', {'rooms': rooms})


# SHOW SINGLE ROOM
def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    return render(request, 'rooms/room_detail.html', {'room': room})

@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.save()
            return redirect('room_list')
    else:
        form = RoomForm()

    return render(request, 'rooms/room_form.html', {'form': form})

@login_required
def edit_room(request, id):
    room = get_object_or_404(Room, id=id, owner=request.user)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_detail', id=room.id)
    else:
        form = RoomForm(instance=room)

    return render(request, 'rooms/room_form.html', {'form': form})

@login_required
def delete_room(request, id):
    room = get_object_or_404(Room, id=id, owner=request.user)

    if request.method == 'POST':
        room.delete()
        return redirect('room_list')

    return render(request, 'rooms/room_confirm_delete.html', {'room': room})
