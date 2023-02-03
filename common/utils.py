from io import BytesIO

from django.core.files.storage import default_storage
from PIL import Image, ImageOps


def image_rotate(image):
    """Correct image orientation based on EXIF meta data."""
    try:
        image = ImageOps.exif_transpose(image)
    except IOError as err:
        print("I/O error: {0}".format(err))
    return image


def image_compress(image, instance):
    """Reduces the overall file size with the original aspect ratio."""
    image.thumbnail((1024, 1024), Image.ANTIALIAS)
    memfile = BytesIO()
    image.save(memfile, "JPEG", optimize=True)
    default_storage.save(instance.photo.name, memfile)
    memfile.close()
    image.close()
