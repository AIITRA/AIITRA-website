from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# try:
#     from django.contrib.auth import get_user_model
#     User = get_user_model()
# except ImportError:
#     from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.png', upload_to='profile_pics')

    # dateofbirth=models.DateField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height >= 200 or img.width >= 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
        if img.width<img.height:
            crop = (img.height-img.width)/2
            cropped_image = img.crop((0, crop, img.width, img.height-crop))
        elif img.width>img.height:
            crop = (img.width-img.height)/2
            cropped_image = img.crop((crop, 0, img.width-crop, img.height))
        else:
            cropped_image=img
        cropped_image.save(self.image.path)

        # if img.width >= 200 and img.height<=200:
        #     output_size = (img.height, img.height)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)
        #
        # elif img.height >= 200 and img.width <= 200:
        #     output_size = (img.width, img.width)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)
        #
        # elif img.height >= 200 and img.width >= 200:
        #     output_size = (200, 200)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)
# Create your models here.
