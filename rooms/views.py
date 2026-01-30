from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib import messages
from .models import Room, RoomImage
from .forms import RoomForm, RegisterForm


# 🏠 ROOM LIST + SEARCH
def room_list(request):
    rooms = Room.objects.all().order_by('-created_at')

    search_query = request.GET.get('q')
    property_type = request.GET.get('property')

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


# 🔍 ROOM DETAIL
def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    return render(request, 'rooms/room_detail.html', {'room': room})


# ➕ ADD ROOM
@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        images = request.FILES.getlist('gallery_images')

        if form.is_valid():
            try:
                room = form.save(commit=False)
                room.owner = request.user
                room.save()

                # Save gallery images
                for img in images:
                    RoomImage.objects.create(room=room, image=img)

                return redirect('room_list')
            except Exception as e:
                messages.error(
                    request,
                    f"Image upload failed. Check Render logs. Error: {str(e)[:200]}"
                )
        else:
            print(form.errors)  # DEBUG if something fails
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")

    else:
        form = RoomForm()

    return render(request, 'rooms/room_form.html', {'form': form})


# ✏ EDIT ROOM
@login_required
def edit_room(request, id):
    room = get_object_or_404(Room, id=id, owner=request.user)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        images = request.FILES.getlist('gallery_images')

        if form.is_valid():
            try:
                form.save()

                # Add new images
                for img in images:
                    RoomImage.objects.create(room=room, image=img)

                # Delete checked images
                delete_ids = request.POST.getlist('delete_images')
                if delete_ids:
                    RoomImage.objects.filter(id__in=delete_ids, room=room).delete()

                return redirect('room_detail', id=room.id)
            except Exception as e:
                messages.error(
                    request,
                    f"Image upload failed. Check Render logs. Error: {str(e)[:200]}"
                )
        else:
            print(form.errors)
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")

    else:
        form = RoomForm(instance=room)

    return render(request, 'rooms/room_form.html', {'form': form})


# ❌ DELETE ROOM
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


# 🔐 LOGIN
class CustomLoginView(LoginView):
    template_name = 'auth/login.html'


# 🚪 LOGOUT CONFIRM
def logout_confirm(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return render(request, 'auth/logout_confirm.html')


# 📊 USER DASHBOARD
@login_required
def dashboard(request):
    my_properties = Room.objects.filter(owner=request.user).order_by('-created_at')

    context = {
        'my_properties': my_properties
    }
    return render(request, 'rooms/dashboard.html', context)


def test_storage(request):
    return HttpResponse(str(default_storage))


# Debug: check if Cloudinary is active on Render (visit /storage-check/ on live site)
def storage_check(request):
    use_clou = getattr(settings, 'USE_CLOUDINARY', False)
    storage_cls = default_storage.__class__.__name__
    cloud_name = getattr(settings, 'CLOUDINARY_CLOUD_NAME', '') or '(not set)'
    text = (
        f"USE_CLOUDINARY: {use_clou}\n"
        f"DEFAULT_FILE_STORAGE class: {storage_cls}\n"
        f"CLOUDINARY_CLOUD_NAME: {cloud_name}\n"
    )
    return HttpResponse(text, content_type='text/plain')