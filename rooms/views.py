from django.shortcuts import render, get_object_or_404, redirect
from .models import Room,RoomImage
from .forms import RoomForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect


def room_list(request):
    rooms = Room.objects.all().order_by('-created_at')

    search_query = request.GET.get('q')
    property_type = request.GET.get('property')

    # 🔥 FIX: ignore empty or "None"
    if search_query and search_query.lower() != "none":
        rooms = rooms.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(property_type__icontains=search_query) |
            Q(room_type__icontains=search_query)
        )

    if property_type:
        rooms = rooms.filter(property_type__iexact=property_type)

    context = {
        'rooms': rooms,
        'selected_property': property_type,
        'search_query': search_query if search_query != "None" else "",
    }
    return render(request, 'rooms/room_list.html', context)



# 🟢 PROPERTY DETAIL
def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    return render(request, 'rooms/room_detail.html', {'room': room})


# ➕ ADD PROPERTY
@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        images = request.FILES.getlist('gallery_images')

        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.save()

            for img in images:
                RoomImage.objects.create(room=room, image=img)

            return redirect('room_list')
    else:
        form = RoomForm()

    return render(request, 'rooms/room_form.html', {'form': form})


# ✏ EDIT PROPERTY
@login_required
def edit_room(request, id):
    room = get_object_or_404(Room, id=id, owner=request.user)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        images = request.FILES.getlist('gallery_images')

        if form.is_valid():
            form.save()

            # ✅ ADD NEW IMAGES
            for img in images:
                RoomImage.objects.create(room=room, image=img)

            # ✅ DELETE CHECKED IMAGES
            delete_ids = request.POST.getlist('delete_images')
            if delete_ids:
                RoomImage.objects.filter(id__in=delete_ids, room=room).delete()

            return redirect('room_detail', id=room.id)
    else:
        form = RoomForm(instance=room)

    return render(request, 'rooms/room_form.html', {'form': form})

# ❌ DELETE PROPERTY
@login_required
def delete_room(request, id):
    room = get_object_or_404(Room, id=id, owner=request.user)

    if request.method == 'POST':
        room.delete()
        return redirect('room_list')

    return render(request, 'rooms/room_confirm_delete.html', {'room': room})


# 👤 REGISTER
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


# 🔐 LOGIN VIEW
class CustomLoginView(LoginView):
    template_name = 'auth/login.html'


# 🚪 LOGOUT CONFIRM
def logout_confirm(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return render(request, 'auth/logout_confirm.html')


@login_required
def dashboard(request):
    my_properties = Room.objects.filter(owner=request.user).order_by('-created_at')

    context = {
        'my_properties': my_properties
    }
    return render(request, 'rooms/dashboard.html', context)

