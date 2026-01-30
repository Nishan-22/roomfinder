"""
Template tag to always return full Cloudinary image URLs in production.
Fixes img src pointing to Render domain (e.g. /rooms/ap1.jpg) instead of Cloudinary.
"""
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def cloudinary_image_url(image_field):
    """
    Return the image URL. When Cloudinary is configured, always build the full
    Cloudinary URL so img src never points to the app domain (e.g. Render).
    """
    if not image_field:
        return ''
    if getattr(settings, 'USE_CLOUDINARY', False):
        from cloudinary import CloudinaryResource
        return CloudinaryResource(image_field.name).url
    return image_field.url
