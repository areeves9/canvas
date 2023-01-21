from io import BytesIO
from django.core.files.storage import default_storage

from PIL import Image, ExifTags


def image_rotate(image):
    """Correct image orientation based on EXIF meta data."""
    try:
        exif_data = image._getexif()
        if exif_data:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == "Orientation":
                    break
            exif = dict(exif_data.items())
            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif_data[orientation] == 8:
                image = image.rotate(90, expand=True)
    except IOError as err:
        print("I/O error: {0}".format(err))
    return image


def image_compress(image, instance):
    """Maintain the aspect ratio of the orginial image with thumbnail."""
    image.thumbnail((1024, 1024), Image.ANTIALIAS)
    memfile = BytesIO()
    image.save(memfile, "JPEG", optimize=True)
    default_storage.save(instance.photo.name, memfile)
    memfile.close()
    image.close()
