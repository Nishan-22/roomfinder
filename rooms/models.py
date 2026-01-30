from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):

    PROPERTY_TYPE_CHOICES = [
        ('Room', 'Room'),
        ('Apartment', 'Apartment'),
        ('Hostel', 'Hostel'),
    ]

    ROOM_TYPE_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Shared', 'Shared'),
        ('1BHK', '1BHK'),
        ('2BHK', '2BHK'),
        ('3BHK', '3BHK'),
    ]

    LOCATION_CHOICES = [
        ('Kathmandu', 'Kathmandu'),
        ('Pokhara', 'Pokhara'),
        ('Biratnagar', 'Biratnagar'),
    ]

    # 👤 Property Owner
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    # 🏠 Property Info
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        default='Room'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField(help_text="Monthly rent in Rs.")
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)

    # 📞 Contact Info
    owner_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    # 📅 Availability
    available_from = models.DateField()

    # 🖼 Main Cover Image (stored in Cloudinary automatically)
    image = models.ImageField(
        upload_to='rooms/',
        blank=True,
        null=True
    )

    # ⏱ Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property_type} - {self.title}"


# 🖼 Multiple Gallery Images
class RoomImage(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='rooms/')

    def __str__(self):
        return f"Image for {self.room.title}"