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
    Return the image URL. Use storage's URL when possible; if it's relative
    (e.g. on Render), build full Cloudinary URL so images load.
    """
    if not image_field:
        return ''
    url = image_field.url
    # If storage returned a relative path, build full Cloudinary URL
    if getattr(settings, 'USE_CLOUDINARY', False) and url.startswith('/'):
        cloud_name = getattr(settings, 'CLOUDINARY_CLOUD_NAME', None)
        if cloud_name:
            url = f'https://res.cloudinary.com/{cloud_name}/image/upload/{url.lstrip("/")}'
    return url
