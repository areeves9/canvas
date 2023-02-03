from PIL import Image

import accounts.models
from canvas.celery import app
from common.utils import image_compress, image_rotate


@app.task()
def process_photo_for_upload(profile_id):
    """Rotate and compress the image file for load."""
    try:
        profile = accounts.models.Profile.objects.get(id=profile_id)
    except accounts.models.Profile.DoesNotExist:
        return {"success": False, "error": f"Profile {profile_id} can not be found."}

    try:
        image = Image.open(profile.photo)
        image_compress(image_rotate(image), profile)

        return {
            "success": True,
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Exception {e} while processing photo for upload to {profile_id}.",
        }
